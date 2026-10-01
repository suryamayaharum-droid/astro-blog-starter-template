export type MuseumCatalogEntry = {
  id: string;
  name: string;
  city: string;
  country: string;
  mode: "live" | "advanced" | "dataset" | "key";
  access: string;
  rights: string;
  apiUrl: string;
  docsUrl: string;
  note: string;
};

export const museumCatalog: MuseumCatalogEntry[] = [
  {
    id: "met",
    name: "The Metropolitan Museum of Art",
    city: "New York",
    country: "EUA",
    mode: "live",
    access: "API pública · sem chave",
    rights: "Use apenas registros com isPublicDomain=true; imagens Open Access podem ser reutilizadas.",
    apiUrl: "https://collectionapi.metmuseum.org/public/collection/v1.1/search",
    docsUrl: "https://metmuseum.github.io/",
    note: "Conectado ao buscador HARUM NOIR. A versão v1.1 é paginada e substitui a busca v1."
  },
  {
    id: "aic",
    name: "Art Institute of Chicago",
    city: "Chicago",
    country: "EUA",
    mode: "live",
    access: "REST + IIIF · sem chave",
    rights: "Filtramos is_public_domain=true; imagens são servidas por IIIF.",
    apiUrl: "https://api.artic.edu/api/v1/artworks/search",
    docsUrl: "https://api.artic.edu/docs/",
    note: "Conectado ao buscador HARUM NOIR com filtro de domínio público."
  },
  {
    id: "cma",
    name: "Cleveland Museum of Art",
    city: "Cleveland",
    country: "EUA",
    mode: "live",
    access: "Open Access API · sem chave",
    rights: "Dados CC0; imagens abertas quando share_license_status=CC0.",
    apiUrl: "https://openaccess-api.clevelandart.org/api/artworks/",
    docsUrl: "https://openaccess-api.clevelandart.org/",
    note: "Conectado ao buscador HARUM NOIR com cc0 + has_image."
  },
  {
    id: "getty",
    name: "J. Paul Getty Museum",
    city: "Los Angeles",
    country: "EUA",
    mode: "advanced",
    access: "Linked Open Data · REST + SPARQL + IIIF",
    rights: "Grande parte dos dados é CC0; direitos das imagens devem ser verificados individualmente.",
    apiUrl: "https://data.getty.edu/museum/collection/sparql",
    docsUrl: "https://data.getty.edu/museum/collection/docs/",
    note: "Preparado para uma segunda integração, ideal para consultas Linked.Art e comparação IIIF."
  },
  {
    id: "rijks",
    name: "Rijksmuseum",
    city: "Amsterdam",
    country: "Países Baixos",
    mode: "advanced",
    access: "Data Services · Linked Data / IIIF",
    rights: "Public Domain/CC0 quando indicado; alguns registros usam CC BY ou permanecem restritos.",
    apiUrl: "https://data.rijksmuseum.nl/",
    docsUrl: "https://data.rijksmuseum.nl/",
    note: "Catálogo aberto de larga escala; integrar por serviços FAIR/IIIF em uma segunda etapa."
  },
  {
    id: "smithsonian",
    name: "Smithsonian Open Access",
    city: "Washington, D.C.",
    country: "EUA",
    mode: "key",
    access: "API pública · chave gratuita",
    rights: "Ativos com marca CC0 podem ser reutilizados; mídia restrita não é exposta como Open Access.",
    apiUrl: "https://api.data.gov/",
    docsUrl: "https://www.si.edu/openaccess/devtools",
    note: "Catalogado, mas não ativado no buscador porque exige API key; não armazenamos credenciais no repositório."
  },
  {
    id: "nga",
    name: "National Gallery of Art",
    city: "Washington, D.C.",
    country: "EUA",
    mode: "dataset",
    access: "Dataset CC0 + imagens Open Access",
    rights: "Dados factuais sob CC0; dezenas de milhares de imagens abertas disponíveis nas fichas das obras.",
    apiUrl: "https://github.com/NationalGalleryOfArt/opendata",
    docsUrl: "https://www.nga.gov/artworks/free-images-and-open-access",
    note: "Fonte excelente para ingestão por lote e curadoria histórica; não depende de uma API de busca para o site."
  },
  {
    id: "smithsonian-github",
    name: "Smithsonian Open Access Dataset",
    city: "Washington, D.C.",
    country: "EUA",
    mode: "dataset",
    access: "GitHub · JSON atualizado",
    rights: "Metadados Open Access e ativos CC0 conforme o registro.",
    apiUrl: "https://github.com/Smithsonian/OpenAccess",
    docsUrl: "https://www.si.edu/openaccess",
    note: "Alternativa sem expor uma chave no cliente; útil para futuras ingestões offline/curadas."
  }
];

export const liveMuseumIds = ["met","aic","cma"] as const;
