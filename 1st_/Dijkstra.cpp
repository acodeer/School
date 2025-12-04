#include<iostream>
#include<vector>
#include<climits>
using namespace std;

const int INF = INT_MAX;
const int V = 7;

int minDistance(vector<int> dist, vector<bool> visited){
    int min = INF, min_index = -1;
    for(int i = 0; i < V; i++){
        if(!visited[i] && dist[i] <= min){
            min = dist[i];
            min_index = i;
        }
    }
    return min_index;
}

void dijkstra(int weight[V][V] , int start){
    vector<int> dist(V, INF); 
    vector<bool> visited(V , false); //방문여부 확인용 벡터배열
    dist[start] = 0;

    for(int i = 0; i < V-1; i++){
        int u = minDistance(dist , visited);
        visited[u] = true;
        for(int j = 0; j < V; j++){
            if()

        }
    }

}

int main(){
    int graph[V][V] = {
        {  0,   5,   6,  10, INF, INF, INF },
        {  5,   0, INF,   7,   8, INF, INF },
        {  6, INF,   0,   8, INF,   7, INF },
        { 10,   7,   8,   0,   9,   6,  10 },
        {INF,   8, INF,   9,   0, INF,  12 },
        {INF, INF,   7,   6, INF,   0,   9 },
        {INF, INF, INF,  10,  12,   9,   0 }
    };
    dijkstra(graph, 0);
    return 0;
}