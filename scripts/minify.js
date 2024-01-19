var htmlminify = require('html-minifier').minify; // HTML
var cssminify = require('csso').minify; // CSS
var UglifyJS = require("uglify-js"); // JS
const fs = require('node:fs');

var htmlindex = fs.readFileSync("sostituzioni/view/templates/index.html", "utf8")
var htmlresult = htmlminify(htmlindex, {
    collapseWhitespace: true,
    removeAttributeQuotes: true,
    removeComments: true,
});


var cssfiles = [
    fs.readFileSync("sostituzioni/view/static/style/colori.css", "utf8"),
    fs.readFileSync("sostituzioni/view/static/style/header.css", "utf8"),
    fs.readFileSync("sostituzioni/view/static/style/index.css", "utf8"),
    fs.readFileSync("sostituzioni/view/static/style/gestionedati.css", "utf8"),
]
var cssindex = cssfiles.join("\n");

var cssresult = cssminify(cssindex, {
    // restructure: false,
});


var code = {
    "fuzzyset.js": fs.readFileSync("sostituzioni/view/static/scripts/lib/fuzzyset.js", "utf8"),
    "compare.js": fs.readFileSync("sostituzioni/view/static/scripts/lib/compare.js", "utf8"),
    "selezione.js": fs.readFileSync("sostituzioni/view/static/scripts/lib/selezione.js", "utf8"),
    "ui.js": fs.readFileSync("sostituzioni/view/static/scripts/ui.js", "utf8"),
    "eventi.js": fs.readFileSync("sostituzioni/view/static/scripts/eventi.js", "utf8"),
    "notizie.js": fs.readFileSync("sostituzioni/view/static/scripts/notizie.js", "utf8"),
    "sostituzioni.js": fs.readFileSync("sostituzioni/view/static/scripts/sostituzioni.js", "utf8"),
    "filtri_sostituzioni.js": fs.readFileSync("sostituzioni/view/static/scripts/filtri_sostituzioni.js", "utf8"),
    "gestione_dati.js": fs.readFileSync("sostituzioni/view/static/scripts/gestione_dati.js", "utf8"),
    "gestione_dati_sostituzione.js": fs.readFileSync("sostituzioni/view/static/scripts/gestione_dati_sostituzione.js", "utf8"),
    "gestione_dati_evento.js": fs.readFileSync("sostituzioni/view/static/scripts/gestione_dati_evento.js", "utf8"),
    "gestione_dati_notizia.js": fs.readFileSync("sostituzioni/view/static/scripts/gestione_dati_notizia.js", "utf8"),
    "onlinesocket.js": fs.readFileSync("sostituzioni/view/static/scripts/onlinesocket.js", "utf8")
};
var jsoptions = {
    mangle: {
        // toplevel: true,
    },
};

var jsresult = UglifyJS.minify(code, jsoptions);


fs.writeFileSync("sostituzioni/view/templates/indexmin.html", htmlresult);
fs.writeFileSync("sostituzioni/view/static/style/indexmin.css", cssresult.css);
fs.writeFileSync("sostituzioni/view/static/scripts/sostituzioni.min.js", jsresult.code);

console.log("Done.")