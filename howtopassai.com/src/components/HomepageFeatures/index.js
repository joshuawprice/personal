import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';


const FeatureList = [
  {
    // title: 'Algorithms',
    Svg: require('@site/static/img/undraw_code_typing_re_p8b9.svg').default,
    description: (
      <Link
        className="button button--secondary button--lg"
        to="/docs/algorithms">
        Algorithms
      </Link>
    ),
  },
  {
    // title: 'Artificial Intelligence',
    Svg: require('@site/static/img/undraw_artificial_intelligence_re_enpp.svg').default,
    description: (
      <Link
        className="button button--secondary button--lg"
        to="/docs/ai">
        Artificial Intelligence
      </Link>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--6')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        {/* <h3>{title}</h3> */}
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
