import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getEnemyDetail } from "../api/enemyApi";

const EnemyDetail = () => {
    const { id } = useParams();
    const { data : enemies, isLoading, error } = useQuery({
        queryKey: ['enemies'],
        queryFn: getEnemyDetail(id),
        enabled: !!id,
    });
    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error loading enemy details</div>;

    return (
        <div>
            <img 
            src={`https://picsum.photos/200/200?random=${id}`} 
            alt="Enemy Image" />
            <h2>Name: {enemies.name}</h2>
            <p>Affiliation: ${enemies.affiliation}</p>
            <p>Class: ${enemies.class_}</p>
            <Link to = "/">Back to Enemy List</Link>
        </div>
    )
}

export default EnemyDetail;