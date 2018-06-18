import axios from 'axios';
import qs from 'qs';
// https://github.com/thereactivestack/react-cookie
import Cookies from 'universal-cookie';


const API_PREFIX = process.env.API_PREFIX || 'http://127.0.0.1:8080';

let loaderOpen, loaderClose;

/**
 * 
 */
const setPostHeaders = () => {
    return {
        headers : {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': (new Cookies()).get('csrftoken')
        }
    }
};

/**
 * Обработка Promise-а загрузки начальных данных
 */
const loaded = (promise, success=null, error=null) => {
    promise.then(response => {
        if (loaderClose) {
            loaderClose();
        }
        if (response.data.code) {
            if (error) {
                error(response.data);
            } else {
                throw response.data.msg;
            }
        } else if (!response.data || !response.data.data) {
            throw 'Ошибка данных сервера';
        } else if (success) {
            success(response.data.data);
        }
    }).catch(error => {
        if (loaderClose) {
            loaderClose();
        }
        alert(error);
    });
};

/**
 * 
 */
const load = (url, params=null, success=null, error=null, method='get') => {
    let promise;
    url = `${API_PREFIX}${url}`;
    if (loaderOpen) {
        loaderOpen();
    }
    if (method == 'get') {
        promise = axios.get(url, {
            params : params
        });
    } else if (method == 'post') {
        promise = axios.post(
            url,
            qs.stringify(params, { indices: false }),
            setPostHeaders()
        );
    }
    if (promise) {
        loaded(promise, success, error);
    }
};

export default {
    example(params, success, error) {
        load('/api/example/', params, success, error, 'post');
    },

    setLoader(open, close) {
        loaderOpen = open;
        loaderClose = close;
    }
}
