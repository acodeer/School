import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getPokemonDetail, getPokemonSpecies } from '../api/pokemonApi'
import { typeColors } from '../utils/typeColors'

export default function PokemonDetail() {
  const { id } = useParams()

  const { data: pokemon, isLoading } = useQuery({
    queryKey: ["pokemon", id],
    queryFn: async () => {
      const detail = await getPokemonDetail(id)
      const species = await getPokemonSpecies(detail.id)
      const koreanName = species.names.find((n) => n.language.name === "ko")?.name
      const flavorText =
        species.flavor_text_entries.find((f) => f.language.name === "ko")?.flavor_text ||
        "(설명이 없습니다.)"

      return {
        id: detail.id,
        name: koreanName || detail.name,
        image: detail.sprites.other["official-artwork"].front_default,
        types: detail.types.map((t) => t.type.name),
        height: detail.height,
        weight: detail.weight,
        stats: detail.stats.map((s) => ({
          name: s.stat.name,
          value: s.base_stat,
        })),
        flavorText,
        generation: species.generation?.name,
        habitat: species.habitat?.name,
      }
    },
  })

  if (isLoading) return <p className="text-center mt-10">불러오는 중...</p>;

  const mainType = pokemon.types[0];
  const headerStyle = typeColors[mainType] || "bg-gray-200 text-black";

  return (
    <div className="p-6 flex flex-col items-center">
      {/* 상단 대표 카드 */}
      <div
        className={`w-full max-w-lg rounded-2xl p-6 mb-6 shadow-md flex flex-col items-center ${headerStyle}`}
      >
        <img
          src={pokemon.image}
          alt={pokemon.name}
          className="w-48 h-48 mb-4 drop-shadow-lg"
        />
        <h2 className="text-3xl font-bold">{pokemon.name}</h2>
        <p className="text-sm opacity-80">#{pokemon.id}</p>
        <div className="flex gap-2 mt-3">
          {pokemon.types.map((t) => (
            <span
              key={t}
              className={`px-3 py-1 rounded-full text-sm font-semibold border-1 ${typeColors[t]}`}
            >
              {t}
            </span>
          ))}
        </div>
      </div>

      {/* 상세 카드 */}
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-md p-6 space-y-6">
        {/* 도감 설명 */}
        <section>
          <h3 className="text-xl font-semibold mb-2">도감 설명</h3>
          <p className="text-gray-700 leading-relaxed whitespace-pre-line">
            {pokemon.flavorText.replace(/\f/g, " ")}
          </p>
        </section>

        {/* 기본 정보 */}
        <section>
          <h3 className="text-xl font-semibold mb-2">기본 정보</h3>
          <div className="grid grid-cols-2 gap-4 text-gray-700">
            <p>키: {pokemon.height / 10} m</p>
            <p>몸무게: {pokemon.weight / 10} kg</p>
            <p>세대: {pokemon.generation}</p>
            <p>서식지: {pokemon.habitat || "알 수 없음"}</p>
          </div>
        </section>

        {/* 능력치 (progress bar) */}
        <section>
          <h3 className="text-xl font-semibold mb-3">능력치</h3>
          <div className="space-y-2">
            {pokemon.stats.map((s) => (
              <div key={s.name}>
                <p className="text-sm font-medium capitalize">{s.name}</p>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`${headerStyle.split(" ")[0]} h-3 rounded-full`}
                    style={{ width: `${(s.value / 200) * 100}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-600">{s.value}</p>
              </div>
            ))}
          </div>
        </section>
      </div>

      <Link
        to="/"
        className="mt-6 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
      >
        돌아가기
      </Link>
    </div>
  )
}