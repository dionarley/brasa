// Remark plugin da documentação: as imagens dos manuais usam a sintaxe do
// pandoc (`![...](renders/x.png){width=58%}`) e apontam para renders gerados
// em dist/v<versão>/renders (fora do git). Aqui:
//
// - `renders/...` vira `/renders/...`, servido de site/static/renders (o
//   docs.sh copia os renders da última liberação antes do build);
// - o `{width=NN%}` que o pandoc entende vira `style="width: NN%"` no <img>,
//   para não aparecer como texto na página.
function walk(node, fn) {
  fn(node);
  if (Array.isArray(node.children)) {
    node.children.forEach((child) => walk(child, fn));
  }
}

module.exports = function remarkDocImages() {
  return (tree) => {
    walk(tree, (node) => {
      if (!Array.isArray(node.children)) {
        return;
      }
      for (let i = node.children.length - 1; i >= 0; i -= 1) {
        const child = node.children[i];
        if (child.type !== 'image') {
          continue;
        }
        if (/^renders\//.test(child.url)) {
          child.url = `/${child.url}`;
        }
        const next = node.children[i + 1];
        const width = next && next.type === 'text'
          ? /^\s*\{width=(\d+(?:\.\d+)?%)\}\s*$/.exec(next.value)
          : null;
        if (width) {
          child.data = child.data || {};
          child.data.hProperties = {
            ...(child.data.hProperties || {}),
            style: `width: ${width[1]}; height: auto;`,
          };
          node.children.splice(i + 1, 1);
        }
      }
    });
  };
};
