#include <iostream>
#include <vector>
#include <climits>
#include <utility> // for pair
#include <queue>   // for priority_queue

using namespace std;
const int INF = INT_MAX;
const int V = 7;

// 인접 리스트를 위한 타입 정의
typedef pair<int, int> iPair; // (가중치, 정점)

void dijkstra(const vector<vector<iPair>>& adj, int start) {
    vector<int> dist(V, INF);        // 시작점으로부터의 최단 거리
    vector<bool> visited(V, false);  // 방문 여부
    vector<int> parent(V, -1);       // 경로 추적을 위한 부모 배열
    
    // 우선순위 큐 (최소 힙) - (거리, 정점) 쌍으로 저장
    priority_queue<iPair, vector<iPair>, greater<iPair>> pq;
    
    dist[start] = 0;
    pq.push(make_pair(0, start));

    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();
        
        if (visited[u]) continue;
        visited[u] = true;

        // u의 모든 인접 정점을 확인
        for (const auto& neighbor : adj[u]) {
            int v = neighbor.second;
            int weight = neighbor.first;

            // 최단 거리 갱신
            if (!visited[v] && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                parent[v] = u;
                pq.push(make_pair(dist[v], v));
            }
        }
    }

    // 최단 경로 계산 결과 출력
    cout << "정점\t최단 거리\t경로" << endl;
    for (int i = 0; i < V; i++) {
        cout << start << " → " << i << "\t" << dist[i] << "\t\t";

        // 경로 역추적
        vector<int> path;
        for (int v = i; v != -1; v = parent[v])
            path.push_back(v);

        for (int j = path.size() - 1; j >= 0; j--) {
            cout << path[j];
            if (j != 0) cout << " → ";
        }
        cout << endl;
    }
}

int main() {
    // 인접 리스트로 그래프 표현
    vector<vector<iPair>> adj(V);
    
    // 정점 0
    adj[0].push_back(make_pair(5, 1));
    adj[0].push_back(make_pair(6, 2));
    adj[0].push_back(make_pair(10, 3));
    
    // 정점 1
    adj[1].push_back(make_pair(5, 0));
    adj[1].push_back(make_pair(7, 3));
    adj[1].push_back(make_pair(8, 4));
    
    // 정점 2
    adj[2].push_back(make_pair(6, 0));
    adj[2].push_back(make_pair(8, 3));
    adj[2].push_back(make_pair(7, 5));
    
    // 정점 3
    adj[3].push_back(make_pair(10, 0));
    adj[3].push_back(make_pair(7, 1));
    adj[3].push_back(make_pair(8, 2));
    adj[3].push_back(make_pair(9, 4));
    adj[3].push_back(make_pair(6, 5));
    adj[3].push_back(make_pair(10, 6));
    
    // 정점 4
    adj[4].push_back(make_pair(8, 1));
    adj[4].push_back(make_pair(9, 3));
    adj[4].push_back(make_pair(12, 6));
    
    // 정점 5
    adj[5].push_back(make_pair(7, 2));
    adj[5].push_back(make_pair(6, 3));
    adj[5].push_back(make_pair(9, 6));
    
    // 정점 6
    adj[6].push_back(make_pair(10, 3));
    adj[6].push_back(make_pair(12, 4));
    adj[6].push_back(make_pair(9, 5));

    dijkstra(adj, 0);
    return 0;
}