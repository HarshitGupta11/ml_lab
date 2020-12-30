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

void solve(){
    int n;
    cin>>n;
    vector<int> h(n);
    vector<int> iq(n);
    for(int i=0;i<n;i++)cin>>h[i];
    for(int i=0;i<n;i++)cin>>iq[i];
    vector<vector<int>> dp(n+1,vector<int> (n+1,1));
    for(int i=0;i<n;i++){
        dp[i][n-1]=1;
    }
    int ans=0;
    for(int i=n-1;i>=0;i--){
        for(int j=n-1;j>=i+1;j--){
            if(h[j]>h[i] && iq[j]<iq[i]){
                dp[i][j]=1+dp[j][j];
                debug(i,j);
            }
            dp[i][j]=max(dp[i][j+1],dp[i][j]);
            ans=max(ans,dp[i][j]);
        }
        debug(dp);
    }
    cout<<ans<<"\n";
    return;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        solve();
    }
    return 0;
}
