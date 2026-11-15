// @ts-check

const {themes} = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Brasa',
  tagline: 'Estanhador 550 W / 127 V — documentação do produto (PS-001)',
  favicon: 'img/brasa-square.svg',

  url: 'http://127.0.0.1:8081',
  baseUrl: '/',

  organizationName: 'dionarley',
  projectName: 'brasa',

  onBrokenLinks: 'warn',
  // Os manuais são Markdown do pandoc (com `{width=…}` nas figuras), não MDX.
  markdown: {
    format: 'md',
    hooks: {
      onBrokenMarkdownLinks: 'warn',
      // As figuras dos manuais são renders da liberação, servidos de
      // static/renders; o plugin remark-doc-images troca renders/ por /renders/.
      onBrokenMarkdownImages: 'ignore',
    },
  },

  i18n: {
    defaultLocale: 'pt-BR',
    locales: ['pt-BR'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          // A raiz é o projeto, não docs/: assim o LEGAL.md (citado pelos
          // manuais como ../../LEGAL.md) entra no site e os links relativos
          // continuam resolvendo. Só docs/**.md e o LEGAL.md são publicados.
          path: '..',
          include: ['docs/**/*.md', 'LEGAL.md'],
          exclude: ['docs/**/*.pdf', 'docs/**/*.txt', 'docs/**/*.csv'],
          routeBasePath: '',
          sidebarPath: require.resolve('./sidebars.js'),
          breadcrumbs: true,
          showLastUpdateTime: false,
          remarkPlugins: [require('./plugins/remark-doc-images')],
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
        pages: {
          path: 'src/pages',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/brasa-square.svg',
      metadata: [
        {
          name: 'description',
          content:
            'Documentação do Brasa (PS-001): manual de uso e segurança, guia de construção, PLM e referências. Estudo não certificado.',
        },
      ],
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Brasa',
        logo: {
          alt: 'Brasa',
          src: 'img/brasa-square.svg',
        },
        items: [
          {to: '/docs/uso/', label: 'Uso e segurança', position: 'left'},
          {to: '/docs/construcao/', label: 'Construção', position: 'left'},
          {to: '/docs/plm/PLANO', label: 'PLM', position: 'left'},
          {to: '/docs/plm/REGISTRO', label: 'Registro mestre', position: 'left'},
          {href: 'http://127.0.0.1:8080', label: 'TeamCraft', position: 'right'},
          {href: 'http://127.0.0.1:8088', label: 'GridCraft', position: 'right'},
          {href: 'http://127.0.0.1:8089', label: 'Desenhos', position: 'right'},
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentação',
            items: [
              {label: 'Manual de uso e segurança', to: '/docs/uso/'},
              {label: 'Guia de construção', to: '/docs/construcao/'},
              {label: 'Registro mestre', to: '/docs/plm/REGISTRO'},
            ],
          },
          {
            title: 'Processo',
            items: [
              {label: 'Plano de ciclo de vida (PLM)', to: '/docs/plm/PLANO'},
              {label: 'TeamCraft: instalação e operação', to: '/docs/plm/TEAMCRAFT'},
              {label: 'Aviso legal e licença', to: '/LEGAL'},
            ],
          },
          {
            title: 'Projeto',
            items: [
              {label: 'Referências', to: '/docs/referencias'},
              {label: 'PS-001 no TeamCraft', href: 'http://127.0.0.1:8080'},
            ],
          },
        ],
        copyright: `Brasa — estudo não certificado. Conteúdo próprio em CC BY-NC-SA 4.0; 127 V é risco de quem executa.`,
      },
      prism: {
        theme: themes.github,
        darkTheme: themes.dracula,
        additionalLanguages: ['bash', 'json', 'diff'],
      },
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 4,
      },
    }),
};

module.exports = config;
