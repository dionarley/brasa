/**
 * Visualizador DXF do Brasa: página mínima em volta de
 * `@mlightcad/cad-simple-viewer` (MIT), que interpreta e desenha DXF/DWG no
 * navegador — sem servidor de arquivos e sem upload.
 *
 * Só DXF é habilitado de propósito: o suporte a DWG no MLightCAD usa o
 * LibreDWG (GPL), que não entra neste projeto. O resto (parsing, geometria,
 * render em WebGL) é o pacote MIT.
 */
import { AcApDocManager, AcEdOpenMode } from '@mlightcad/cad-simple-viewer'

import './style.css'

const viewerEl = document.getElementById('cad-viewer') as HTMLElement
const hint = document.getElementById('hint') as HTMLElement
const statusEl = document.getElementById('status') as HTMLElement
const nameEl = document.getElementById('file-name') as HTMLElement
const fileInput = document.getElementById('file-input') as HTMLInputElement
const selectEl = document.getElementById('drawing-select') as HTMLSelectElement

// Fontes e blocos de título vêm do CDN público do projeto por padrão (o mesmo
// caminho do demo oficial). Para uso offline, sirva os arquivos e aponte
// VITE_CAD_BASE_URL para eles no build.
const BASE_URL =
  (import.meta.env.VITE_CAD_BASE_URL as string | undefined) ??
  'https://cdn.jsdelivr.net/gh/mlightcad/cad-data@main/'

const workerUrl = new URL('workers/mtext-renderer-worker.js', document.baseURI).href

const readOptions = {
  minimumChunkSize: 1000,
  mode: AcEdOpenMode.Read,
  // Sem render progressivo: o desenho aparece de uma vez, já enquadrado.
  progressiveRendering: false
}

function setStatus(text: string, kind: 'ok' | 'busy' | 'error' = 'ok') {
  statusEl.textContent = text
  statusEl.dataset.kind = kind
}

function setFileName(name: string | null) {
  nameEl.textContent = name ?? 'nenhum desenho aberto'
  nameEl.title = name ?? ''
  hint.hidden = Boolean(name)
  selectEl.value = name ?? ''
}

const manager = AcApDocManager.createInstance({
  container: viewerEl,
  autoResize: true,
  baseUrl: BASE_URL,
  // MTEXT é desenhado na thread principal (menos memória que o worker).
  useMainThreadDraw: true,
  webworkerFileUrls: { mtextRender: workerUrl },
  simpleUi: {
    host: viewerEl,
    toolbar: { placement: 'right', items: 'default' },
    dockPanel: { defaultOpen: false, defaultWidth: 280, defaultHeight: 240 }
  }
})

if (!manager) {
  setStatus('não foi possível iniciar o visualizador', 'error')
}

async function openUrl(url: string, name: string) {
  setStatus(`abrindo ${name}…`, 'busy')
  setFileName(name)
  try {
    const ok = await manager!.openUrl(url, readOptions)
    setStatus(ok ? `${name} aberto` : `${name}: não encontrado`, ok ? 'ok' : 'error')
    if (!ok) setFileName(null)
  } catch (error) {
    console.error(error)
    setStatus(`erro ao abrir ${name}`, 'error')
    setFileName(null)
  }
}

async function openFile(file: File) {
  if (!/\.dxf$/i.test(file.name)) {
    setStatus(`${file.name}: só .dxf é aceito aqui`, 'error')
    return
  }
  setStatus(`abrindo ${file.name}…`, 'busy')
  setFileName(file.name)
  try {
    const buffer = await file.arrayBuffer()
    const ok = await manager!.openDocument(file.name, buffer, readOptions)
    setStatus(ok ? `${file.name} aberto` : `${file.name}: não foi possível abrir`, ok ? 'ok' : 'error')
    if (!ok) setFileName(null)
  } catch (error) {
    console.error(error)
    setStatus(`erro ao abrir ${file.name}`, 'error')
    setFileName(null)
  }
}

// Desenhos publicados em drawings/ (o cad_viewer.sh mantém o index.json).
async function loadPublished() {
  try {
    const response = await fetch(new URL('drawings/index.json', document.baseURI), { cache: 'no-cache' })
    if (!response.ok) return
    const names: unknown = await response.json()
    if (!Array.isArray(names) || names.length === 0) return

    selectEl.replaceChildren(new Option('desenhos publicados…', ''))
    for (const name of names as string[]) {
      selectEl.append(new Option(name, name))
    }
    selectEl.hidden = false
    selectEl.addEventListener('change', () => {
      const name = selectEl.value
      if (name) void openUrl(new URL(`drawings/${encodeURIComponent(name)}`, document.baseURI).href, name)
    })
    // Se o ?file= abriu um desenho publicado, deixa o seletor nele.
    selectEl.value = nameEl.title
  } catch {
    // sem drawings/index.json: fica só o seletor de arquivo do navegador
  }
}

// ?file=drawings/prancha.dxf — usado pelo cad_viewer.sh view.
const requested = new URLSearchParams(window.location.search).get('file')
if (requested) {
  const url = new URL(requested, document.baseURI).href
  void openUrl(url, decodeURIComponent(url.split('/').pop() ?? url))
}

fileInput.addEventListener('change', () => {
  const file = fileInput.files?.[0]
  if (file) void openFile(file)
  fileInput.value = ''
})

document.getElementById('hint-pick')?.addEventListener('click', () => fileInput.click())

for (const type of ['dragenter', 'dragover']) {
  window.addEventListener(type, (event) => {
    event.preventDefault()
    document.body.dataset.drag = 'true'
  })
}
window.addEventListener('drop', (event) => {
  event.preventDefault()
  delete document.body.dataset.drag
  const file = (event as DragEvent).dataTransfer?.files?.[0]
  if (file) void openFile(file)
})
window.addEventListener('dragleave', (event) => {
  if (event.target === document.documentElement) delete document.body.dataset.drag
})

void loadPublished()
