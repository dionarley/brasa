import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';

const cards = [
  {
    to: '/docs/uso/',
    code: 'PS-001-US-001',
    title: 'Manual de uso e segurança',
    desc: 'Como usar o estanhador, limites, riscos de 127 V e o que fazer em caso de falha.',
  },
  {
    to: '/docs/construcao/',
    code: 'PS-001-CO-001',
    title: 'Guia de construção',
    desc: 'Sequência de montagem, critérios de aceitação e ensaios do estudo.',
  },
  {
    to: '/docs/plm/PLANO',
    code: 'PS-001-PL-001',
    title: 'Plano de ciclo de vida',
    desc: 'Processo, estados, papéis, revisões e liberação de documentos por ECO.',
  },
  {
    to: '/docs/plm/REGISTRO',
    code: 'PS-001-PL-002',
    title: 'Registro mestre',
    desc: 'Índice controlado: código, revisão vigente, estado e arquivo de cada documento.',
  },
  {
    to: '/docs/plm/TEAMCRAFT',
    code: 'PS-001-PL-003',
    title: 'TeamCraft',
    desc: 'Instalação, operação, MCP e backup do PDM local que guarda as revisões.',
  },
  {
    to: '/docs/referencias',
    code: 'RE',
    title: 'Referências',
    desc: 'Fontes consultadas, autoria e o que cada uma contribuiu para o projeto.',
  },
];

function Home() {
  const wide = useBaseUrl('img/brasa-wide.svg');
  return (
    <Layout
      title="Brasa — estanhador 550 W / 127 V"
      description="Documentação do Brasa (PS-001): uso, construção, PLM e referências."
    >
      <header className="hero-brasa">
        <div className="container text--center">
          <img className="hero-logo" src={wide} alt="Brasa" />
          <h1>Estanhador 550 W / 127 V</h1>
          <p className="lead">
            Documentação do projeto <strong>Brasa</strong> (código interno{' '}
            <code>PS-001</code>): um estudo de reconstrução de pistola de solda a
            partir de transformador de micro-ondas, com modelo 3D, montagem e
            controle de revisões no TeamCraft.
          </p>
          <div className="hero-actions">
            <Link className="button button--primary button--lg" to="/docs/uso/">
              Começar pelo manual de uso
            </Link>
            <Link className="button button--secondary button--lg" to="/docs/plm/REGISTRO">
              Registro mestre
            </Link>
          </div>
        </div>
      </header>

      <main className="container">
        <div className="doc-cards">
          {cards.map((card) => (
            <Link className="doc-card" key={card.to} to={card.to}>
              <span className="doc-card-code">{card.code}</span>
              <span className="doc-card-title">{card.title}</span>
              <span className="doc-card-desc">{card.desc}</span>
            </Link>
          ))}
        </div>

        <div className="notice-brasa">
          <strong>Estudo não certificado.</strong> O Brasa é uma reconstrução
          amadora documentada, sem certificação de segurança, e não um produto
          para venda. A rede de 127 V é risco de choque, incêndio e queimadura:
          leia o <Link to="/docs/uso/">manual de uso e segurança</Link> e o{' '}
          <Link to="/LEGAL">aviso legal</Link> antes de construir ou ligar.
        </div>
      </main>
    </Layout>
  );
}

export default Home;
