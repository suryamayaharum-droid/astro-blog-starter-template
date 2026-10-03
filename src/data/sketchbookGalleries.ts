export const sketchbookGalleries = [
  {
    id: "eva-gonzales-sketchbook",
    artist: "Eva Gonzalès",
    title: "Sketchbook · 86 páginas / 45 desenhos",
    date: "meados da década de 1860",
    medium: "Tinta, lápis, aquarela e guache sobre papel",
    source: "National Gallery of Art",
    rights: "Domínio público — mídia indicada pela NGA",
    principle: "O caderno como espaço íntimo de tentativa: materiais diferentes convivem sem obrigação de acabamento ou unidade artificial.",
    originalUrl: "https://www.nga.gov/artworks/231554-sketchbook",
    commonsUrl: "https://www.nga.gov/artworks/231554-sketchbook",
    images: [
      { url: "https://api.nga.gov/iiif/23718807-32d6-496d-8b7f-b6059cef05b9/full/!800,800/0/default.jpg", href: "https://www.nga.gov/artworks/231554-sketchbook", label: "Capa / abertura" },
      { url: "https://api.nga.gov/iiif/eea210cd-f248-40f1-9567-1c5bb761833e/full/!800,800/0/default.jpg", href: "https://www.nga.gov/artworks/231554-sketchbook", label: "Folha 01" },
      { url: "https://api.nga.gov/iiif/794871b0-1ec4-4b1c-b76b-79f529aee1a0/full/!800,800/0/default.jpg", href: "https://www.nga.gov/artworks/231554-sketchbook", label: "Folha 02" }
    ]
  },
  {
    id: "toulouse-lautrec-album-de-marine",
    artist: "Henri de Toulouse-Lautrec",
    title: "Album de Marine",
    date: "1879–80",
    medium: "Grafite, aquarela e giz preto sobre papel",
    source: "The Metropolitan Museum of Art + Wikimedia Commons",
    rights: "Domínio público",
    principle: "Caderno como sequência de pensamento: observação, variação e memória antes da obra final.",
    originalUrl: "https://www.metmuseum.org/art/collection/search/334729",
    commonsUrl: "https://commons.wikimedia.org/wiki/Category:Album_de_Marine_(58.130)_by_Henri_de_Toulouse-Lautrec",
    images: [
      { file: "Album_de_Marine-_Sketchbook_of_48_folios_containing_17_watercolors_and_27_black_chalk_and_graphite_sketches_MET_260901.jpg", label: "Fólio 01" },
      { file: "Album_de_Marine-_Sketchbook_of_48_folios_containing_17_watercolors_and_27_black_chalk_and_graphite_sketches_MET_260932.jpg", label: "Fólio 02" },
      { file: "Album_de_Marine-_Sketchbook_of_48_folios_containing_17_watercolors_and_27_black_chalk_and_graphite_sketches_MET_260897.jpg", label: "Fólio 03" }
    ]
  },
  {
    id: "william-trost-richards-sketchbook-vii",
    artist: "William Trost Richards",
    title: "Sketchbook VII · paisagem e mar",
    date: "1886",
    medium: "Grafite e tinta sobre papel",
    source: "The Metropolitan Museum of Art + Wikimedia Commons",
    rights: "Domínio público / arquivos Commons CC0",
    principle: "Repetir o motivo sem repetir a imagem: nuvem, mar, rocha e árvore viram laboratório de ritmo, pressão e síntese.",
    originalUrl: "https://www.metmuseum.org/art/collection/search/15382",
    commonsUrl: "https://commons.wikimedia.org/wiki/Category:Drawings_by_William_Trost_Richards",
    images: [
      { file: "Sketch_of_Clouds_and_Sea_(from_Sketchbook_VII)_MET_257794.jpg", label: "Nuvens e mar" },
      { file: "Sketch_of_a_Breaking_Wave_(from_Sketchbook_VII)_MET_257793.jpg", label: "Onda · estudo I" },
      { file: "Sketch_of_Breaking_Waves_(from_Sketchbook_VII)_MET_257796.jpg", label: "Ondas · estudo II" },
      { file: "Seascape_with_Breaking_Waves_(from_Sketchbook_VII)_MET_257791.jpg", label: "Mar em ruptura" },
      { file: "Sketch_of_Trees_(Clouds%3F)_(from_Sketchbook_VII)_MET_257761.jpg", label: "Árvores / nuvens" }
    ]
  }
] as const;

export const commonsImage = (file: string, width = 900) =>
  `https://commons.wikimedia.org/wiki/Special:Redirect/file/${file}?width=${width}`;
