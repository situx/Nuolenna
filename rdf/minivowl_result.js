var minivowlresult={
 "info": [
  {
   "description": "Created with pyowl2vowl (version 0.1) as part of the SPARQLing Unicorn QGIS Plugin"
  }
 ],
 "nodes": [
  {
   "name": "ObjectProperty",
   "type": "class",
   "uri": "http://www.w3.org/2002/07/owl#ObjectProperty"
  },
  {
   "name": "DatatypeProperty",
   "type": "class",
   "uri": "http://www.w3.org/2002/07/owl#DatatypeProperty"
  },
  {
   "name": "Ontology",
   "type": "class",
   "uri": "http://www.w3.org/2002/07/owl#Ontology"
  },
  {
   "name": "GraphemeComposition",
   "type": "class",
   "uri": "http://purl.org/graphemon/GraphemeComposition"
  },
  {
   "name": "Grapheme",
   "type": "class",
   "uri": "http://purl.org/graphemon/Grapheme"
  },
  {
   "name": "GraphemeList",
   "type": "class",
   "uri": "http://purl.org/graphemon/GraphemeList"
  },
  {
   "name": "Class",
   "type": "class",
   "uri": "http://www.w3.org/2002/07/owl#Class"
  },
  {
   "name": "GraphemeReading",
   "type": "class",
   "uri": "http://purl.org/graphemon/GraphemeReading"
  },
  {
   "name": "GraphemeSense",
   "type": "class",
   "uri": "http://purl.org/graphemon/GraphemeSense"
  },
  {
   "name": "Epoch",
   "type": "class",
   "uri": "http://purl.org/cuneiform/Epoch"
  }
 ],
 "links": [
  {
   "source": 3,
   "target": 3,
   "valueTo": "hasPart",
   "propertyTo": "class",
   "uriTo": "http://purl.org/graphemon/hasPart"
  },
  {
   "source": 3,
   "target": 4,
   "valueTo": "hasPart",
   "propertyTo": "class",
   "uriTo": "http://purl.org/graphemon/hasPart"
  },
  {
   "source": 4,
   "target": 3,
   "valueTo": "hasPart",
   "propertyTo": "class",
   "uriTo": "http://purl.org/graphemon/hasPart"
  },
  {
   "source": 4,
   "target": 4,
   "valueTo": "hasPart",
   "propertyTo": "class",
   "uriTo": "http://purl.org/graphemon/hasPart"
  },
  {
   "source": 3,
   "target": 7,
   "valueTo": "hasGraphemeReading",
   "propertyTo": "class",
   "uriTo": "http://purl.org/graphemon/hasGraphemeReading"
  },
  {
   "source": 4,
   "target": 7,
   "valueTo": "hasGraphemeReading",
   "propertyTo": "class",
   "uriTo": "http://purl.org/graphemon/hasGraphemeReading"
  },
  {
   "source": 5,
   "target": 3,
   "valueTo": "member",
   "propertyTo": "class",
   "uriTo": "http://www.w3.org/2000/01/rdf-schema#member"
  },
  {
   "source": 5,
   "target": 4,
   "valueTo": "member",
   "propertyTo": "class",
   "uriTo": "http://www.w3.org/2000/01/rdf-schema#member"
  },
  {
   "source": 3,
   "target": 8,
   "valueTo": "sense",
   "propertyTo": "class",
   "uriTo": "http://lemon-model.net/lemon#sense"
  },
  {
   "source": 4,
   "target": 8,
   "valueTo": "sense",
   "propertyTo": "class",
   "uriTo": "http://lemon-model.net/lemon#sense"
  },
  {
   "source": 7,
   "target": 9,
   "valueTo": "epoch",
   "propertyTo": "class",
   "uriTo": "http://purl.org/graphemon/epoch"
  }
 ]
}