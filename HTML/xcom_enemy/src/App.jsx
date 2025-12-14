import { useState , useEffect } from 'react'
import {useQuery} from '@tanstack/react-query'
import {Routes , Route} from 'react-router-dom'
import EnemyList from './pages/EnemyList.jsx'
import EnemyDetail from './pages/EnemyDetail.jsx'
import { getEnemies } from './api/enemyApi.js'


function App() {
  const {data : enemies , isLoading , error} = useQuery({
    queryKey: ['enemies'],
    queryFn: getEnemies,
  })

  if(isLoading) return <div>Loading...</div>
  if(error) return <div>Error loading enemies</div>
  return(
    <Routes>
      <Route path="/" element = {<EnemyList enemies ={enemies} />} />
      <Route path="/enemy/:id" element = {<EnemyDetail enemies ={enemies} />} />
    </Routes>
  )
  /*const [enemy , setEnemy] = useState([])

  useEffect(() => {
    const fetchEnemies = async () => {
      try{
        const data = await getEnemies()
        setEnemy(data)
      }
      catch(err) {
        console.error('Failed to fetch enemies:', err)
      }
    }
    fetchEnemies()
  },[])
  return (
    <Routes>
      <Route path="/" element={<EnemyList enemies={enemies} />} />
      <Route path="/enemy/:id" element={<EnemyDetail enemies={enemies} />} />
    </Routes>
  )*/
}
export default App
