import axios from 'axios';

// const base_url = process.env.ENV_URL || 'http://www.default.com';

// const dev = process.env.NEXT_PUBLIC_ENV_URL !== 'production';

const uploadFile = async (file, option) => {
  // if production
  // const url = `${process.env.NEXT_PUBLIC_BASE_URL}/api/processfile`;
  // production url
  // const url = 'http://localhost:8080/api/processfile';
  // const url = 'http://146.190.19.45:8080/api/processfile';

  const url = 'https://magic-extractor-v2.herokuapp.com/api/processfile';

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
  })
    .catch((error) => {
      // count number of requests
      // count successful requests
      // cuont failed requests - if any fail say how many
      // and display it on the screen where the luxury goods component is
      console.log('error', error);
      // return 'error state';
    });
    // return success if successful at the top
    // count requests

  // .catch((AxiosError) => {
  //   if (error instanceof Error) {
  //     console.error(
  //       'Error with fetching ..., details: ',
  //       error,
  //     );
  //   }
  // });
  return response;
};

export default uploadFile;
