# filter-md-files-to-another-directory

This GitHub Action copies a file from the current repository to a location in another repository
During the copy process, markdown files having a Jekyll's style frontmatter will be filtered (not copied) 
if they match one of thoses criterias :

* if a `hide` attribute exists and is set to true
* if a `notbefore` attribute exists and is set to a date in the future (date format `YYYY-MM-DD`)

The main usage of this action is to publish to a public repository **only** ready to release articles 
from a private repository, while still backing up every single modification within the private repository.

```yaml
name: Publish content to public repo

on: push

jobs:
  check-bats-version:
    runs-on: ubuntu-latest
    steps:
    
    - name: Checkout Private repo (this one)
    - uses: actions/checkout@v3
      with:
        path: private-repo
    
    - name: Checkout Public repo (where files will be copied)
      uses: actions/checkout@v3
      with:
        repository: rebrec/rebsecnotes-public
        token: ${{ secrets.GH_PAT }} # `GH_PAT` is a secret that contains your PAT
        path: public-repo

    - name: Copy to public repository directory while filtering not ready to release .md files
      uses: rebrec/filter-md-files-to-another-directory@main
        with:
          destination: 'private-repo/docs'
          destination_folder: 'public-repo/docs'

    - run: |
        git config user.name github-actions
        git config user.email github-actions@github.com
        git add .
        git commit -m "generated"
        git push
```
