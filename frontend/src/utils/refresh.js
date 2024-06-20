import axios from 'axios';
import Cookies from 'js-cookie';

const refreshToken = async () => {
if (!Cookies.get('refresh_token')) {
    return;
    }
  try {
    const response = await axios.post('http://localhost:8002/api/v1/auth/refresh', {}, {
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'Authorization': `Bearer ${Cookies.get('refresh_token')}`, // Включаем refresh_token из кук в заголовок
      },
    });

    const { access_token, refresh_token } = response.data;

    Cookies.set('access_token', access_token, { expires: 1 / 48 });
    Cookies.set('refresh_token', refresh_token);

  } catch (error) {

  }
};

const scheduleRefreshToken = () => {
  setInterval(refreshToken, 15 * 60 * 1000);
} ;

export default scheduleRefreshToken;