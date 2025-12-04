import axios from 'axios'

const api = axios.create({
  baseURL: 'https://pokeapi.co/api/v2',
})

export const getPokemonList = async (limit = 30) => {
  const res = await api.get(`/pokemon?limit=${limit}`)
  return res.data.results
}

export const getPokemonDetail = async (name) => {
  const res = await api.get(`/pokemon/${name}`)
  return res.data
}

export const getPokemonSpecies = async (id) => {
  const res = await api.get(`/pokemon-species/${id}`)
  return res.data
}
