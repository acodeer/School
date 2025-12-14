import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8080/api/enemies',
})

export const getEnemies = async () => {
    const res = await api.get(``)
    return res.data;
}
export const getEnemyDetail = async (id) => {
    const res = await api.get(`/${id}`)
    return res.data;
}