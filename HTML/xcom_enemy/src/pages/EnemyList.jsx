import {Link} from "react-router-dom"
import EnemyCard from "../components/EnemyCard.jsx"

export default function EnemyList({enemies}) {
  return (
    <>
    {enemies.map((enemy) => (
        <EnemyCard key = {enemy.id} enemy={enemy}/>
            ))}
    </>
  )
}