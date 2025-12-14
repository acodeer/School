import { Link } from "react-router-dom";

export default function EnemyCard({enemy}){
    return (
        <Link to = {`/enemy/${enemy.id}`}
        className="" >
            <img
            src={`https://picsum.photos/200/200?random=${enemy.id}`}
            alt="Enemy Image"/>
            <h2>{enemy.name}</h2>
        </Link>
    )
}