# Extra command line tools for rdflib

This package provides some additional command line tools for rdflib:

* SPARQL Query execution with optional reasoning using [OWL-RL](https://github.com/RDFLib/OWL-RL):
    ```bash
    rdflib-xtl sparql --help
    ```
* OWL Reasoning using [OWL-RL](https://github.com/RDFLib/OWL-RL)
    ```bash
    rdflib-xtl reason --help
    ```

Usage examples:

```bash
# Install pipx
pip3 install --user --upgrade pipx

# (optionally) clear pipx cache if you want the latest version ...
\rm -vr ~/.local/pipx/.cache/

# check version
pipx run --spec yocho.rdflib-xtl rdflib-xtl --version

# Run SPARQL without reasoning ...
pipx run --spec yocho.rdflib-xtl \
  rdflib-xtl sparql \
  -q 'SELECT * WHERE { ?s rdfs:subClassOf owl:Thing. }' \
  http://xmlns.com/foaf/spec/index.rdf

# Dump input graph with SPARQL query ...
pipx run --spec yocho.rdflib-xtl \
  rdflib-xtl sparql \
  -q 'CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }' \
  http://xmlns.com/foaf/spec/index.rdf

# Run SPARQL with reasoning ...
pipx run --spec yocho.rdflib-xtl \
  rdflib-xtl sparql --reason \
  -q 'SELECT * WHERE { ?s rdfs:subClassOf owl:Thing. }' \
  http://xmlns.com/foaf/spec/index.rdf

# Dump reasoned graph with SPARQL query ...
pipx run --spec yocho.rdflib-xtl \
  rdflib-xtl sparql --reason \
  -q 'CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }' \
  http://xmlns.com/foaf/spec/index.rdf

# Run reasoning ...
pipx run --spec yocho.rdflib-xtl \
  rdflib-xtl reason http://xmlns.com/foaf/spec/index.rdf
```
