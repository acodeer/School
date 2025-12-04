 import { useQuery } from '@tanstack/react-query'
import PokemonCard from '../components/PokemonCard'
import { getPokemonList, getPokemonDetail, getPokemonSpecies } from '../api/pokemonApi'

export default function PokemonList() {

  const { data: pokemons, isLoading, isError, error } = useQuery({
    queryKey: ['pokemons'],
    queryFn: async () => {
      const list = await getPokemonList(1025)

      // Promise.all : 여러 비동기 작업을 병렬로 처리하고, 모든 작업이 완료될 때까지 기다림
      return Promise.all(
        list.map(async (p) => {

          const detail = await getPokemonDetail(p.name)
          const species = await getPokemonSpecies(detail.id);
          const koreanName = species.names.find((n) => n.language.name === "ko")?.name;

          //console.log(detail.types)
          //console.log(detail.types.map((t) => t.type.name))

          return {
            id: detail.id,
            name: koreanName || detail.name,
            image: detail.sprites.other["official-artwork"].front_default,
            // types 배열에서 타입 이름만 추출하여 새로운 배열을 만들고 반환
            types: detail.types.map((t) => t.type.name),
          }
        })
      )
    },
  })

  if (isLoading) {
    return <p className="text-center mt-10">Loading...</p>
  }

  if (isError) {
    return <p className="text-center mt-10">오류 발생: {error.message}</p>
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-center mb-6">포켓몬 도감</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {pokemons.map((p) => (
          <PokemonCard key={p.id} pokemon={p} />
        ))}
      </div>
    </div>
  )
}