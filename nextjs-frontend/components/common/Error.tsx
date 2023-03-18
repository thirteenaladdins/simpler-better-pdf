import React from 'react';

interface ErrorProps {
  errors: string[];
}

const Error: React.FC<ErrorProps> = ({ errors }) => (
  <div>
    {errors.map((error, index) => (
      <pre key={index}>{error}</pre>
    ))}
  </div>
);

export default Error;
