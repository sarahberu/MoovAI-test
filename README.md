# Agent d'analyse de marché

Un agent IA qui orchestre plusieurs outils d'analyse pour produire des rapports d'intelligence de marché structurés pour des produits e-commerce.

## Architecture

Le système utilise une **orchestration Python native** plutôt qu'un framework comme LangGraph ou CrewAI. Ce choix est délibéré pour le contexte de cet exercice de 3 à 6 heures : une implémentation native démontre un contrôle explicite sur le flux d'exécution, rend les contrats de données entre les outils visibles et testables, et évite la surcharge d'abstraction d'un framework. Dans une application en production, un framework comme LangGraph serait plus approprié pour gérer la parallélisation et la reprise sur erreur (voir étape 6).

```
POST /analyze
     │
     ▼
 FastAPI (validation)
     │
     ▼
 Orchestrateur
     ├─ 1. Web Scraper Tool     → prix, concurrents, avis (simulés)
     ├─ 2. Sentiment Analyzer   → LLM extrait le sentiment des avis
     └─ 3. Report Generator     → LLM synthétise le rapport stratégique
     │
     ▼
 Réponse JSON structurée
```

Chaque outil a une interface claire, retourne un output structuré et peut être remplacé indépendamment. L'orchestrateur passe les données séquentiellement : le scraper alimente l'outil de sentiment, et les deux alimentent le générateur de rapport.

### Pourquoi des données simulées

Le scraper utilise des données mockées plutôt que du scraping web en temps réel pour plusieurs raisons pratiques. D'abord, le scraping sans permission explicite est légalement ambigu et varie selon les conditions d'utilisation de chaque plateforme. Ensuite, la plupart des grands détaillants (Amazon, BestBuy) bloquent activement les scrapers automatisés avec des firewalls, des CAPTCHAs et des limites de taux, ce qui rendrait les tests peu fiables. Finalement, les données mockées permettent des tests reproductibles et une démonstration de l'architecture sans dépendances externes ou coûts d'API. Dans un contexte de production, le scraper serait remplacé par une intégration avec une API de scraping autorisée.

## Installation

### Prérequis

- Python 3.13+
- Le fichier `api/.env` (fourni séparément via un lien sécurisé)

### Installation locale

```bash
git clone <repo-url>
cd MoovAI-test

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# Placer le fichier api/.env fourni à la racine du projet
```

### Démarrer l'API

```bash
uvicorn app.main:app --reload
```

L'API est disponible à `http://localhost:8000`.

### Démarrer avec Docker

```bash
# Placer le fichier api/.env fourni à la racine du projet

docker-compose up --build
```

## Utilisation

### Vérification de santé

```bash
curl http://localhost:8000/health
```

### Analyser un produit

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Oura Ring Gen 3", "market": "Canada"}'
```

### Exemple de réponse

```json
{
  "executive_summary": "The Oura Ring Gen 3 holds a strong premium position in the Canadian wearables market...",
  "pricing_analysis": {
    "retailers": {
      "Amazon.ca":      { "price_cad": 452.49, "in_stock": true, "platform_rating": 4.3, "review_count": 1842, "shipping": "Free with Prime" },
      "BestBuy.ca":     { "price_cad": 461.99, "in_stock": true, "platform_rating": 4.1, "review_count": 523,  "shipping": "Free shipping over $35" },
      "Official Store": { "price_cad": 429.99, "in_stock": true, "platform_rating": 4.5, "review_count": 980,  "shipping": "Free standard shipping" }
    },
    "prices_by_retailer": { "Amazon.ca": 452.49, "BestBuy.ca": 461.99, "Official Store": 429.99 },
    "average_price": 448.16,
    "price_range": { "min": 429.99, "max": 461.99 },
    "price_positioning": "Premium pricing consistent with the brand's positioning as a health-focused wearable..."
  },
  "competitive_landscape": {
    "main_competitors": [
      { "name": "Samsung Galaxy Ring", "price_cad": 549.99, "retailer": "BestBuy.ca", "category": "fitness ring" },
      { "name": "RingConn Smart Ring",  "price_cad": 349.99, "retailer": "Amazon.ca",  "category": "fitness ring" },
      { "name": "Ultrahuman Ring AIR",  "price_cad": 399.99, "retailer": "Amazon.ca",  "category": "fitness ring" }
    ],
    "market_position": "Mid-to-upper tier, undercutting Samsung while commanding a premium over budget alternatives.",
    "competitive_advantages": ["Superior sleep tracking accuracy", "Titanium build quality", "Subscription-free tier available"]
  },
  "sentiment_analysis": {
    "overall_sentiment": "positive",
    "sentiment_score": 0.78,
    "strengths": ["Sleep tracking accuracy", "Battery life", "Discreet form factor"],
    "weaknesses": ["Subscription cost", "No display", "Sizing process"],
    "value_positioning": "premium"
  },
  "strategic_recommendations": [
    "Introduce a Canadian loyalty or referral program to improve retention.",
    "Negotiate preferred placement on Amazon.ca to close the gap with Samsung's visibility.",
    "Address subscription concerns in Canadian marketing with a 3-month free trial offer.",
    "Expand ring sizing availability in BestBuy.ca to reduce return rates."
  ]
}
```

Un exemple complet de rapport généré est disponible dans [examples/sample_report.json](examples/sample_report.json).

## Tests

```bash
pytest
```

24 tests répartis dans 5 fichiers. Chaque fichier cible une couche distincte de l'application :

- **`test_scraper.py`** (7 tests) : schéma de sortie, passthrough produit/marché, prix positifs, structure des concurrents, présence des avis, champs des détaillants, structure des spécifications
- **`test_sentiment.py`** (4 tests) : clés de schéma requises, score dans [0.0, 1.0], forces/faiblesses sont des listes non vides, le LLM est appelé avec le bon nom de produit et les avis dans le prompt
- **`test_report.py`** (2 tests) : clés de schéma requises, le prompt LLM contient le nom du produit et le marché
- **`test_orchestrator.py`** (7 tests) : les trois outils sont appelés une fois chacun ; l'output du scraper est transmis au sentiment ; l'output du sentiment est transmis au rapport ; les erreurs de chaque outil se propagent sans être avalées
- **`test_api.py`** (5 tests) : le endpoint health retourne 200, `/analyze` retourne 200 avec tous les champs requis, un marché invalide retourne 422, une panne du pipeline retourne 500

Les outils LLM (sentiment, rapport) sont testés avec un client Anthropic mocké, donc aucun appel API réel n'est effectué et les tests s'exécutent hors ligne.

---

## Étape 4, Architecture de données et stockage

### Pourquoi stocker les données intermédiaires ?

La première question à se poser, c'est : est-ce qu'on stocke juste le rapport final, ou aussi les données brutes collectées en cours de route ?

Si on ne garde que le rapport final, on est limités : dès qu'un utilisateur veut ajuster le format, changer la structure ou raffiner les recommandations, il faut tout refaire depuis le début, re-scraper, rappeler le LLM, attendre. C'est long et coûteux.

En stockant séparément les données du scraper (prix, concurrents) et les commentaires collectés, on peut **régénérer le rapport à partir de ce qu'on a déjà** sans retourner sur le web. Ça donne la flexibilité à l'utilisateur d'itérer sur le résultat sans repartir de zéro à chaque fois.

### Schéma proposé

Trois tables suffisent pour couvrir les besoins :

```sql
-- Données brutes collectées par le scraper
scraper_data (
  id            UUID PRIMARY KEY,
  product_name  TEXT,
  market        TEXT,
  data          JSONB,        -- prix, concurrents, specs
  collected_at  TIMESTAMPTZ
)

-- Commentaires et avis collectés
reviews (
  id            UUID PRIMARY KEY,
  product_name  TEXT,
  market        TEXT,
  reviews       JSONB,        -- liste des avis bruts
  collected_at  TIMESTAMPTZ
)

-- Rapport final généré à partir des données ci-dessus
analyses (
  id              UUID PRIMARY KEY,
  product_name    TEXT,
  market          TEXT,
  scraper_data_id UUID REFERENCES scraper_data(id),
  reviews_id      UUID REFERENCES reviews(id),
  report          JSONB,      -- rapport structuré complet
  model_used      TEXT,
  created_at      TIMESTAMPTZ,
  duration_ms     INTEGER
)
```

Le rapport est stocké en JSONB parce que sa structure peut varier, certains produits ont plus de concurrents, certains marchés ont plus de données de prix. Une colonne JSON est plus adaptée qu'une table ultra-normalisée pour ce genre de contenu variable.

### Logs d'exécution

Pour un outil interne simple, on n'a pas besoin d'un système de logging élaboré. L'essentiel, c'est de savoir si quelque chose a planté et combien de temps chaque étape a pris :

```sql
-- Trace d'exécution légère, surtout utile pour déboguer
tool_runs (
  id           UUID PRIMARY KEY,
  analysis_id  UUID REFERENCES analyses(id),
  tool_name    TEXT,          -- scraper | sentiment | report
  duration_ms  INTEGER,
  error        TEXT           -- null si succès
)
```

### Gestion des configurations d'agents

La configuration d'un agent, ça recouvre deux niveaux bien distincts.

Le premier, c'est la **configuration technique globale** : quel modèle LLM utiliser, la température, le nombre max de tokens. Ça ne change pas à la volée, ça vit dans des variables d'environnement et c'est versionné avec le code. Pas besoin de DB pour ça.

Le deuxième niveau, c'est la **personnalisation des rapports**. La mise en situation parle d'analyses "automatisées et personnalisées", et c'est là que ça devient intéressant. Si un utilisateur veut un rapport focalisé sur les prix plutôt que sur le sentiment client, ou un format plus condensé, ou une autre langue, il faut que le système puisse s'adapter sans tout reconfigurer manuellement.

Pour ça, on stocke les configurations de rapport en base de données :

```sql
-- Profils de configuration pour la génération des rapports
report_configs (
  id            UUID PRIMARY KEY,
  name          TEXT,           -- ex: 'rapport_executif', 'analyse_prix'
  focus         TEXT[],         -- ex: ['pricing', 'competitors', 'sentiment']
  format        TEXT,           -- 'detailed' | 'summary' | 'bullets'
  language             TEXT,           -- 'fr' | 'en'
  custom_instructions  TEXT,           -- directives libres injectées dans le prompt
  active               BOOLEAN,
  created_at    TIMESTAMPTZ
)
```

La table `analyses` référence ensuite le profil utilisé (`report_config_id`), ce qui permet de savoir exactement quelle configuration a produit quel rapport.

Ce design se combine bien avec le stockage des données intermédiaires : si l'utilisateur change de profil de rapport, on peut **régénérer le rapport depuis les données scrappées déjà en base**, sans retourner sur le web ni rappeler les outils de collecte. La personnalisation est gratuite en termes de coût LLM si les données sont déjà là.

### Système de stockage recommandé

- **PostgreSQL** (base de données principale) : support JSONB pour les rapports flexibles, écosystème mature et fiable
- **Redis** (cache) : lecture rapide des données récentes par produit et marché

### Cache des données collectées

Le scraping est l'étape la plus coûteuse du pipeline, en temps et potentiellement en coût si on utilise une vraie API de scraping. Mettre les données collectées en cache évite de tout refaire à chaque analyse pour un produit déjà connu.

Redis est utilisé comme couche de lecture rapide, en complément de PostgreSQL. Quand une analyse est demandée, on vérifie d'abord le cache :

```
scraper:{product_name}:{market}   →  données du dernier scraping
reviews:{product_name}:{market}   →  commentaires du dernier scraping
```

Si les données sont en cache, on saute le scraping et on génère directement le rapport. PostgreSQL reste la source de vérité : les données y sont toujours persistées, Redis n'est qu'un accès rapide à ce qu'on a déjà.

L'invalidation est gérée **à la demande** : c'est l'utilisateur qui décide quand ses données sont périmées et qu'il veut relancer un scraping. Pas de TTL automatique. C'est un choix délibéré pour un outil interne : les prix et les avis ne changent pas à la seconde, et l'utilisateur est le mieux placé pour savoir si son analyse du matin est encore pertinente l'après-midi.

---

## Étape 5 : Monitoring et observabilité

### Tracer l'exécution des agents

Dans un système d'agents enchaînés, savoir *où* quelque chose a ralenti ou planté est essentiel. Sans visibilité par étape, on obtient juste "l'analyse a échoué", sans savoir si c'est le scraper, l'appel LLM ou la génération du rapport.

L'approche est d'instrumenter chaque outil avec des blocs chronométrés dans l'orchestrateur. Des standards comme OpenTelemetry permettent de capturer ces traces de façon uniforme, puis de les visualiser dans un outil adapté. Le résultat : une timeline par requête qui montre quel outil a été appelé, combien de temps il a pris, et s'il a retourné une erreur.

### Collecter les métriques de performance

Les métriques permettent de voir des tendances que les logs seuls ne montrent pas, comme une dégradation graduelle de la latence sur plusieurs heures. Les plus importantes à suivre :

- La durée totale du pipeline (vue globale de l'expérience utilisateur)
- La durée de chaque outil individuellement (pour isoler ce qui ralentit)
- Le taux d'erreur par outil (pour distinguer une panne du scraper d'un problème LLM)
- Le taux de cache hits (une chute soudaine indique souvent un problème côté cache)
- Le volume de requêtes par code de statut (pour détecter une hausse anormale d'erreurs)

### Alerter en cas de dysfonctionnement

Pour un outil interne, des logs bien structurés consultés régulièrement peuvent suffire dans un premier temps. Ce qui compte, c'est d'avoir défini à l'avance ce qui est "anormal" : un taux d'erreur qui monte brusquement suggère une API externe en difficulté, une latence qui s'emballe pointe vers un ralentissement LLM, et zéro analyses réussies sur une période en heures de bureau est un signal critique. Si le système devient plus sollicité, on branche un mécanisme de notification sur ces seuils.

### Visibilité pour le client

L'équipe technique a accès aux logs et aux métriques détaillées, mais le client e-commerce a besoin d'une façon de voir que le système fonctionne sans avoir accès à l'infrastructure. Deux approches simples permettent de le faire sans sur-ingéniérer.

La première est d'enrichir le endpoint `/health` existant pour qu'il expose un état lisible : pas juste "le serveur répond", mais aussi si le dernier scraping a réussi, si l'API LLM est joignable, et un résumé du taux de succès récent. Le client peut interroger cet endpoint directement ou le brancher à son propre système de monitoring.

La deuxième est un dashboard en lecture seule exposant les métriques clés : taux de succès des analyses, latence moyenne, dernières requêtes. Des outils comme Grafana permettent de partager une vue publique ou protégée par lien sans donner accès aux logs sous-jacents. Le client voit l'essentiel, l'équipe garde le contrôle sur le reste.

### Mesurer la qualité des outputs

Ce point est développé à l'étape 7 dans le cadre de l'amélioration continue.

---

## Étape 6 : Scaling et optimisation

L'architecture actuelle est intentionnellement simple : un orchestrateur Python natif qui appelle les outils en séquence, une requête à la fois. C'est suffisant pour l'exercice, mais pas pour un système en production. Voici comment on ferait évoluer ça.

### Gérer des pics de charge

Le premier problème avec le design synchrone actuel : chaque appel à `POST /analyze` bloque jusqu'à ce que tout le pipeline soit terminé. À 100 requêtes simultanées, ça sature.

La solution est de découpler l'acceptation de la requête de son exécution. L'API répond immédiatement avec un identifiant de tâche, et le pipeline s'exécute en arrière-plan :

```
POST /analyze       →  retourne { task_id } immédiatement
GET  /results/{id}  →  retourne le rapport quand terminé
```

Pour l'exécution en arrière-plan, une queue de tâches (comme Celery avec Redis comme broker) permet à plusieurs workers de traiter des analyses indépendamment. Ajouter de la capacité devient alors une question d'ajouter des workers. L'API et les workers sont sans état, donc le scaling horizontal est direct.

### Framework d'orchestration pour la production

L'orchestrateur natif Python est transparent et simple à déboguer, mais il gère mal la parallélisation et la reprise sur erreur. Pour un système en production, un framework comme **LangGraph** serait plus adapté : il représente le pipeline comme un graphe où les noeuds sans dépendance peuvent s'exécuter en parallèle, avec une gestion native des états intermédiaires et des retries.

### Paralléliser les tâches d'analyse

Dans le pipeline actuel, le scraper collecte tout en séquence : prix, concurrents, puis reviews. Pourtant, ces deux collectes sont indépendantes l'une de l'autre. On pourrait les confier à deux agents distincts qui tournent simultanément, puis convergent avant l'analyse de sentiment :

```
Agent scraper (prix + concurrents)  ──┐
                                       ├──→ Sentiment → Rapport
Agent scraper (reviews)             ──┘
```

Si chaque scraping prend 5 secondes, on passe de 10 secondes à 5 secondes sur cette étape, sans changer la logique du reste du pipeline.

### Optimiser les coûts LLM

Deux leviers principaux : appeler le LLM moins souvent, et choisir le bon modèle par tâche.

Pour appeler moins souvent : le cache est la première ligne. Si les données scrappées sont déjà en cache, on peut aussi mettre en cache les résultats intermédiaires du LLM. Si le même produit est analysé deux fois avec les mêmes avis, l'analyse de sentiment ne devrait pas être recalculée.

Pour choisir le bon modèle : l'analyse de sentiment, c'est une extraction structurée sur un texte court : un modèle léger fait très bien ça à une fraction du coût. La génération du rapport final demande plus de raisonnement et justifie un modèle plus capable. Aligner le modèle sur la complexité de la tâche peut réduire les coûts de moitié sans toucher à la qualité.

---

## Étape 7 : Amélioration continue et A/B testing

### Évaluer automatiquement la qualité des analyses (LLM as Judge)

Un pipeline techniquement fonctionnel peut quand même produire de mauvais rapports si un prompt a régressé. Le tracing et les métriques ne captent pas ça : ils mesurent si le système tourne, pas si ce qu'il produit est bon.

L'approche : après chaque analyse, un second appel LLM évalue le rapport généré sur des critères précis (est-ce que les recommandations sont concrètes, est-ce que l'analyse est spécifique au produit et au marché, est-ce que le résumé est cohérent). Les scores sont stockés en base et suivis dans le temps. Si la moyenne baisse après un changement de prompt, on le voit avant que l'utilisateur ne s'en plaigne.

Ce n'est pas de la surveillance en temps réel, c'est un signal de régression automatisé qui remplace la révision manuelle.

### Comparer différentes stratégies de prompt

Pour savoir si un nouveau prompt est meilleur, on compare sur les mêmes données : générer des rapports avec l'ancien et le nouveau prompt sur un même jeu de cas, puis comparer les scores LLM as Judge. Si le nouveau score mieux de façon consistante, on le déploie.

Si on veut tester en conditions réelles sans tout basculer, on peut faire un déploiement progressif où une fraction des analyses utilise le nouveau prompt et le reste l'ancien, puis comparer les scores sur une période avant de trancher. Le LLM as Judge fournit la métrique de comparaison dans les deux cas.

### Feedback loop utilisateur

Un endpoint `POST /feedback` permet à l'utilisateur de noter le rapport et d'ajouter un commentaire. Les notes basses flagguent automatiquement le rapport pour révision humaine.

Les rapports révisés et annotés constituent un **gold set**, un ensemble de cas de référence qu'on utilise pour valider tout changement de prompt avant de le déployer. Un nouveau prompt doit produire des scores équivalents ou supérieurs sur ces cas. C'est une façon simple d'éviter les régressions sans avoir besoin de tester manuellement chaque variation.

### Faire évoluer les capacités des agents

C'est là où l'architecture modulaire paye concrètement. Ajouter un nouvel outil (un analyseur de tendances de marché, un outil de veille concurrentielle) ne nécessite que trois choses :

1. Créer `app/tools/nouveau_outil.py` avec une fonction qui retourne un dict structuré
2. Ajouter un appel dans `app/orchestrator/agent.py`
3. Ajouter le champ correspondant dans `app/models/response.py`

Aucun outil existant n'est touché, l'API ne change pas. L'architecture absorbe les nouvelles capacités sans friction.
