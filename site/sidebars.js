// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    {
      type: 'category',
      label: 'Uso e segurança',
      link: {type: 'doc', id: 'docs/uso/USO'},
      items: ['docs/uso/USO'],
    },
    {
      type: 'category',
      label: 'Construção',
      link: {type: 'doc', id: 'docs/construcao/CONSTRUCAO'},
      items: ['docs/construcao/CONSTRUCAO'],
    },
    {
      type: 'category',
      label: 'PLM',
      link: {type: 'doc', id: 'docs/plm/PLANO'},
      items: [
        'docs/plm/PLANO',
        'docs/plm/REGISTRO',
        'docs/plm/TEAMCRAFT',
      ],
    },
    {
      type: 'category',
      label: 'Referências',
      items: ['docs/referencias'],
    },
    {
      type: 'category',
      label: 'Projeto e direitos',
      items: ['LEGAL'],
    },
  ],
};

module.exports = sidebars;
