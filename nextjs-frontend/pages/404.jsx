// just create a file "404.js" in pages folder.

// import 404.css
import React from 'react';

// pages/404.js
export default function Custom404() {
  return (
    <div className="mCont">
      <h1>404</h1>

      <section>
        <p>Page could not be found.</p>
      </section>
    </div>
  );
}
