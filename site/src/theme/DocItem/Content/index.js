import React from 'react';
import Original from '@theme-original/DocItem/Content';
import {useDoc} from '@docusaurus/plugin-content-docs/client';

// Faixa de documento controlado: código, revisão, estado e data vêm do front
// matter dos arquivos em docs/, que continuam sendo a fonte única (a mesma que
// tools/plm/build.sh transforma em PDF).
export default function Content(props) {
  const {frontMatter} = useDoc();
  const {docid, revision, status, date, subtitle} = frontMatter || {};
  const show = Boolean(docid || revision || subtitle);

  return (
    <>
      {show && (
        <div className="doc-meta" role="note">
          {docid && <span className="doc-meta-code">{docid}</span>}
          {revision && (
            <span>
              revisão <strong>{revision}</strong>
            </span>
          )}
          {status && <span className="doc-meta-status">{status}</span>}
          {date && <span>{date}</span>}
          {subtitle && <span className="doc-meta-sub">{subtitle}</span>}
        </div>
      )}
      <Original {...props} />
    </>
  );
}
