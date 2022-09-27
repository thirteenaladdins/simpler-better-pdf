import axios from 'axios';

// const base_url = process.env.ENV_URL || 'http://www.default.com';

// const dev = process.env.NEXT_PUBLIC_ENV_URL !== 'production';

const uploadFile = async (file, option) => {
  // if production
  // const url = `${process.env.NEXT_PUBLIC_BASE_URL}/api/processfile`;
  // production url
  const url = 'http://146.190.19.45:8080/api/processfile';

  // for production
  // set the base url in the .env file
  // const url = 'https://luxury-goods-backend.herokuapp.com/api/processfile';

  // for docker - productionyar
  // const url = '/api/processfile';

  const formData = new FormData();
  // console.log('formdata', option);
  formData.append('file', file);
  formData.append('option', option);

  const response = await axios.post(url, formData, {
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  });
    // .catch((err) => {
    //   if (err.response.status === 500) {
    //     console.log('Something went wrong')
    //   }
    // })

  return response;
};

export default uploadFile;
