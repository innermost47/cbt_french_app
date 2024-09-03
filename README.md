# CBT French App

CBT French App est une application mobile destinée à la restructuration cognitive (TCC). Conçue pour aider les utilisateurs à traverser des situations difficiles en restructurant leurs pensées, cette application propose un moyen simple de créer et de gérer des sessions de TCC. De plus, elle offre la possibilité de partager ces sessions avec un psychologue ou un autre contact de confiance.

## Fonctionnalités

- **Création de Sessions de TCC** : L'application permet aux utilisateurs de créer des sessions détaillées pour restructurer leurs pensées, en répondant à une série de questions guidées.

- **Gestion des Contacts** : Ajoutez, modifiez et supprimez facilement des contacts dans l'application. Associez un nom, un prénom, un e-mail et un rôle (par exemple, "Psychologue", "Ami", etc.) à chaque contact.

- **Partage des Sessions** : Sélectionnez des contacts pour partager vos sessions de TCC. Envoyez facilement les détails de la session par e-mail directement depuis l'application.

- **Compatibilité Android** : Fonctionne parfaitement sous Android 13. Si vous rencontrez des problèmes d'autocomplétion, nous recommandons d'utiliser le clavier Gboard de Google.

## Installation

1. **Prérequis** :

   - Un appareil fonctionnant sous Android 13.
   - L'application Buildozer et les outils SDK Android configurés pour le développement sous Android.

2. **Cloner le projet** :

   ```bash
   git clone https://github.com/innermost47/cbt_french_app.git
   cd cbt_french_app
   ```

3. **Construire l'APK** :

   - Assurez-vous que votre environnement est configuré pour Buildozer.
   - Construisez l'APK avec la commande suivante :
     ```bash
     buildozer -v android debug
     ```

4. **Installer l'APK** :
   - Une fois l'APK construit, vous pouvez l'installer directement sur votre appareil Android :
     ```bash
     buildozer android deploy run
     ```

## Utilisation

1. **Créer une nouvelle session** :

   - Depuis le menu principal, sélectionnez "Nouvelle Session".
   - Répondez aux questions guidées pour structurer votre session de TCC.

2. **Ajouter un contact** :

   - Accédez à l'écran de gestion des contacts depuis le menu.
   - Ajoutez un contact en spécifiant son nom, prénom, e-mail et rôle.

3. **Partager une session** :
   - Sélectionnez une session dans la liste.
   - Choisissez les contacts avec lesquels vous souhaitez partager la session.
   - Confirmez l'envoi de l'e-mail.

## Problèmes connus

- **Problème d'autocomplétion** :
  - Si vous rencontrez des difficultés avec l'autocomplétion lors de la saisie de texte, veuillez installer et utiliser le clavier Gboard de Google pour une meilleure expérience utilisateur.

## Téléchargement de l'APK

Si vous ne souhaitez pas construire l'application vous-même, vous pouvez télécharger l'APK directement depuis la section "Releases" de ce dépôt GitHub.

### Étapes pour télécharger et installer l'APK :

1. **Accédez à la section "Releases"** :

   - Rendez-vous sur la [page des Releases](https://github.com/innermost47/cbt_french_app/releases) de ce dépôt GitHub.

2. **Téléchargez la dernière version** :

   - Sous la dernière version publiée, vous trouverez un fichier APK prêt à être installé. Cliquez sur le fichier APK pour le télécharger.

3. **Installer l'APK sur votre appareil Android** :

   - Une fois le fichier téléchargé, ouvrez-le sur votre appareil Android pour commencer l'installation.
   - Si c'est la première fois que vous installez une application en dehors du Google Play Store, vous devrez autoriser l'installation d'applications à partir de sources inconnues.

4. **Lancer l'application** :
   - Une fois l'installation terminée, vous pouvez ouvrir l'application et commencer à l'utiliser.

## Fonctionnalité Hors Ligne et Stockage des Données

L'application **CBT French App** est conçue pour fonctionner entièrement hors ligne. Toutes les sessions que vous créez sont enregistrées localement sur votre téléphone. Cela signifie que vous pouvez utiliser l'application sans connexion Internet, ce qui garantit la confidentialité de vos données et permet une utilisation dans n'importe quelle situation.

### Détails du stockage :

- **Stockage local** : Toutes les données de vos sessions (y compris les réponses aux questions de restructuration cognitive) sont sauvegardées directement sur votre appareil. Aucune donnée n'est envoyée sur le cloud ou un serveur distant sans votre consentement.

- **Fonctionnalité hors ligne** : L'application continue de fonctionner normalement même sans connexion Internet. Vous pouvez consulter, créer et éditer des sessions à tout moment.

- **Partage des sessions** : Si vous choisissez de partager une session par e-mail, l'application utilisera les services de messagerie de votre appareil pour envoyer les données. Si vous préférez ne pas partager vos sessions, vous pouvez les conserver uniquement pour votre usage personnel.

Cette fonctionnalité hors ligne est idéale pour ceux qui souhaitent utiliser l'application dans des environnements où l'accès à Internet est limité ou pour ceux qui préfèrent garder leurs données strictement privées.

## Support

Pour toute question ou demande d'assistance, veuillez contacter [anthony.charretier@gmail.com].
