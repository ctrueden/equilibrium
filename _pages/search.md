---
title: Search
---
<script src="https://unpkg.com/lunr/lunr.js"></script>

<style>
.highlight {
    color: red;
    font-weight: bold;
}
.icon {
    max-width: 8rem;
    max-height: 8rem;
}
.result {
    display: inline-block;
    padding: 0.3em;
}
.result a {
    color: yellow;
}
.result-title {
    width: 500px;
    overflow: hidden;
    text-align: center;
    font-variant: small-caps;
    background-color: #357;
    color: yellow;
}
.result-icon {
    display: inline-block;
    height: 128px;
    width: 128px;
    background-color: #ccc;
    padding-left: 1px;
    text-align: center;
    vertical-align: middle;
}
.result-icon img {
    max-width: 100%;
    max-height: 100%;
}
.result-snippet {
    display: inline-block;
    height: 118px;
    width: 361px;
    padding: 5px;
    overflow: hidden;
    vertical-align: middle;
    background-color: #ccc;
}
</style>

<input type="text" id="search" placeholder="Type to search...">
<div id="results"></div>

<script>
let documents = null;
let idx = null;

// Front-matter keys that are structural/meta rather than searchable content.
const SKIP_FIELDS = new Set([
    'case', 'id', 'image', 'image-source', 'layout', 'link', 'link2',
    'review_needed', 'session-number', 'session-date', 'datestamp', 'when', 'wiki'
]);

// Strip obvious Markdown/HTML markup so neither the index nor the displayed
// snippets carry literal syntax like [text](url), **bold**, or `code`.
function stripMarkup(s) {
    return s
        .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1') // images -> alt text
        .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')  // links -> link text
        .replace(/<[^>]+>/g, ' ')                 // HTML tags
        .replace(/^\s*#{1,6}\s+/gm, '')           // ATX heading markers
        .replace(/^\s*>\s?/gm, '')                // blockquote markers
        .replace(/^\s*[-+*]\s+/gm, '')            // list bullets
        .replace(/[*_`~]/g, '')                   // emphasis / code markers
        .replace(/\s+/g, ' ')                     // collapse whitespace
        .trim();
}

// Recursively flatten a value into searchable text. Strings are stripped of
// markup; arrays and objects (e.g. memorable_moments, scenes, npcs) are walked
// and joined so their nested prose becomes searchable too.
function collectText(value) {
    if (typeof value === 'string') return stripMarkup(value);
    if (Array.isArray(value)) return value.map(collectText).join(' ');
    if (value && typeof value === 'object') {
        return Object.entries(value)
            .filter(([k]) => !SKIP_FIELDS.has(k))
            .map(([, v]) => collectText(v))
            .join(' ');
    }
    return '';
}

document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('assets/docs.json');
    documents = await response.json();

    // Flatten every doc once: title stays its own field (for ranking boost),
    // searchText is everything else (body + all front-matter content).
    documents.forEach(doc => { doc.searchText = collectText(doc); });

    idx = lunr(function () {
        this.ref('id');
        this.field('title', { boost: 10 });
        this.field('searchText');

        documents.forEach(function (doc) {
            this.add(doc);
        }, this);
    });

    // Handle search-as-you-type
    document.getElementById('search').addEventListener('input', function () {
        const query = this.value.trim();
        const results = query === '' ? null : idx.search(query);
        displayResults(query, results, documents);
    });
});

function createIcon(doc) {
    if (doc.image === undefined) {
        // TODO: Find good default icons.
        if (doc.id.startsWith("creatures/")) {
        }
        else if (doc.id.startsWith("dossiers/")) {
        }
        else if (doc.id.startsWith("events/")) {
        }
        else if (doc.id.startsWith("locales/")) {
        }
        return ``;
    }
    return `<img src="${doc.image}">`;
}

function extractContextSnippet(body, query) {
    // Thanks, ChatGPT! :-)
    const contextLength = 100; // Adjust context length as needed
    const queryRegex = new RegExp(`\\b(${query.split(/\s+/).join('|')})\\b`, 'gi');
    const matchIndex = body.search(queryRegex);

    if (matchIndex === -1) {
        return ''; // Query terms not found in document
    }

    let start = Math.max(0, matchIndex - contextLength);
    let end = Math.min(body.length, matchIndex + contextLength);

    // Adjust start and end to ensure we have whole words
    while (start > 0 && !/\s/.test(body[start])) {
        start--;
    }
    while (end < body.length && !/\s/.test(body[end])) {
        end++;
    }

    let snippet = body.substring(start, end).trim();

    // Highlight matching terms with <span> tags
    snippet = snippet.replace(queryRegex, '<span class="highlight">$&</span>');

    return snippet;
}

function displayResults(query, results, documents) {
    const resultsContainer = document.getElementById('results');

    if (results === null) {
        resultsContainer.innerHTML = '';
    }
    else if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No results found</p>';
    }
    else {
        resultsContainer.innerHTML = `<p>${results.length} results found</p>`;
        results.forEach(result => {
            const doc = documents.find(d => d.id === result.ref);
            const icon = createIcon(doc);
            const snippet = extractContextSnippet(doc.searchText, query);
            const item = document.createElement('div');
            item.className = 'result';
            item.innerHTML =
                `<a href="${doc.id}">` +
                `<div class="result-title">${doc.title}</div>` +
                `<div class="result-icon">${icon}</div>` +
                `</a>` +
                `<div class="result-snippet">${snippet}</div>`;
            resultsContainer.appendChild(item);
        });
    }
}
</script>
