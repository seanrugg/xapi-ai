# Registering https://w3id.org/xapi-ai/

`ids/xapi-ai/` here is the identifier directory for [perma-id/w3id.org](https://github.com/perma-id/w3id.org). It passes that repository's checker (`tools/check`, 42 rules). Submit it after this repo's `main` serves the Pages site (w3id reviewers check that the target is live).

From a terminal with `gh` signed in:

```sh
gh repo fork perma-id/w3id.org --clone -- --depth 1
cd w3id.org
git checkout -b add-xapi-ai
mkdir -p ids/xapi-ai
curl -fsSL https://raw.githubusercontent.com/seanrugg/xapi-ai/main/w3id/ids/xapi-ai/.htaccess -o ids/xapi-ai/.htaccess
curl -fsSL https://raw.githubusercontent.com/seanrugg/xapi-ai/main/w3id/ids/xapi-ai/README.md -o ids/xapi-ai/README.md
ls -a ids/xapi-ai          # both files must be there
git add ids/xapi-ai
git commit -m "Add /xapi-ai/: persistent IRIs for the xAPI AI Agent Actions Profile"
git push -u origin add-xapi-ai
gh pr create --repo perma-id/w3id.org --head seanrugg:add-xapi-ai --fill
```

What the rules do: `/xapi-ai/profile` (and `/profile/0.10.0`) returns `profile.json` to JSON and JSON-LD clients and the documentation page to browsers (303); each concept IRI, such as `/xapi-ai/verbs/perceived`, returns the profile JSON or the page at that concept's anchor; anything else goes to the documentation page.
