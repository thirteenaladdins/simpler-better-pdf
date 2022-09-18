import axios from 'axios';

const uploadFile = async (file, option) => {
  const url = 'http://localhost:8080/api/processfile';
  // for production
  // const url = 'https://luxury-goods-backend.herokuapp.com/api/processfile';
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
