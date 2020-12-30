#pragma GCC optimize("Ofast")
#pragma GCC target("avx,avx2,fma")
#pragma GCC optimization ("unroll-loops")

#include <bits/stdc++.h>

using namespace std;

void __print(int x) {cerr << x;}
void __print(long x) {cerr << x;}
void __print(long long x) {cerr << x;}
void __print(unsigned x) {cerr << x;}
void __print(unsigned long x) {cerr << x;}
void __print(unsigned long long x) {cerr << x;}
void __print(float x) {cerr << x;}
void __print(double x) {cerr << x;}
void __print(long double x) {cerr << x;}
void __print(char x) {cerr << '\'' << x << '\'';}
void __print(const char *x) {cerr << '\"' << x << '\"';}
void __print(const string &x) {cerr << '\"' << x << '\"';}
void __print(bool x) {cerr << (x ? "true" : "false");}

template<typename T, typename V>
void __print(const pair<T, V> &x) {cerr << '{'; __print(x.first); cerr << ','; __print(x.second); cerr << '}';}
template<typename T>
void __print(const T &x) {int f = 0; cerr << '{'; for (auto &i: x) cerr << (f++ ? "," : ""), __print(i); cerr << "}";}
void _print() {cerr << "]\n";}
template <typename T, typename... V>
void _print(T t, V... v) {__print(t); if (sizeof...(v)) cerr << ", "; _print(v...);}
#ifndef ONLINE_JUDGE
#define debug(x...) cerr << "[" << #x << "] = ["; _print(x)
#else
#define debug(x...)
#endif
#define ll long long int

int dp;
vector<vector<int>> gr(1e4+10);
int inf=1e7+10;

void dfs(int vert,int to_find,int depth=0){
    debug(vert);
    if(vert==to_find){
        dp=depth;
        return;
    }
    debug(gr[vert]);
    for(auto node:gr[vert]){
        dfs(node,to_find,depth+1);
    }
}

void solve(){
    int n;
    cin>>n;
    int vert_a,vert_b;
    cin>>vert_a>>vert_b;
    int max_nodes;
    for(int i=0;i<n;i++){
        int u,v;
        cin>>u>>v;
        u--,v--;
        gr[u].push_back(v);
    }
    int min_val=1e8;
    int node=-1;
    dp=inf;
    dfs(vert_a-1,vert_b-1);
    if(dp!=inf){
        cout<<"-1\n";
        return;
    }
    dp=inf;
    dfs(vert_b-1,vert_a-1);
    if(dp!=inf){
        cout<<"-1\n";
        return;
    }
    for(int i=0;i<n;i++){
        if(i!=vert_a-1 && i!=vert_b-1){
            ll s=0;
            dp=inf;
            dfs(i,vert_a-1);
            s+dp;
            if(dp!=inf){
                dp=inf;
                dfs(i,vert_b-1);
                if(dp!=inf){
                    s+=dp;
                    if(s<min_val){
                        debug("Found",i);
                        min_val=s;
                        node=i+1;
                    }
                }
            }
        }
    }
    cout<<node<<"\n";
    return;
}


int main(){
    int t;
    t=1;
    while(t--){
        solve();
    }
    return 0;
}
