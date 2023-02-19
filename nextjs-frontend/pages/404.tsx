// just create a file "404.tsx" in pages folder.

// import 404.css
import React from 'react';

// pages/404.tsx
const Custom404: React.FC = () => {
  return (
    <div className="mCont">
      <h1>404</h1>

      <section>
        <p>Page could not be found.</p>
      </section>
    </div>
  );
};

export default Custom404;
