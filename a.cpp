#include <bits/stdc++.h>

using namespace std;

// string tracesAreSimilar(vector<int> S,vector<int> T){
//     //cout<<S.size()<<T.size()<<"\n";
//     if(S.size()!=T.size()){
//         return "NO";
//     }
//     vector<int> sc(1024,0);
//     vector<int> tc(1024,0);
//     for(int i=0;i<S.size();i++){
//         sc[S[i]+512]+=1;
//         tc[T[i]+512]+=1;
//     }
//     for(int i=0;i<1024;i++){
//         if(abs(sc[i]-tc[i])>3){
//             return "NO";
//         }
//     }
//     return "YES";
// }

// vector<int> tradeCounts(vector<int> systemA,vector<int> systemB){
//     int n=systemA.size();
//     int m=systemB.size();
//     sort(systemA.begin(),systemA.end());
//     vector<int> ans;
//     for(int i=0;i<m;i++){
//         int val=upper_bound(systemA.begin(),systemA.end(),systemB[i])-systemA.begin();
//         ans.push_back(val);
//     }
//     //cout<<ans.size()<<"\n";
//     return ans;
// }

// int pairCount(vector<int> nums){
//     int n=nums.size();
//     for(int i=0;i<n;i++)nums[i]=nums[i]%100;
//     vector<int> a(200,0);
//     for(int i=0;i<n;i++)a[nums[i]]++;
//     int ans=0;
//     for(int i=0;i<100;i++){
//         if(i==50){
//             ans+=min(a[i],a[100-i])/2;
//         }
//         else{
//             ans+=min(a[i],a[100-i]);
//         }
//         a[i]=0;
//     }
//     return ans;
// }

int countUniv(vector<int> a){
    int n=a.size();
    vector<int> nms;
    int c=1;
    for(int i=1;i<n;i++){
        if(a[i]!=a[i-1]){
            nms.push_back(c);
            c=1;
        }
        else{
            c++;
        }
    }
    nms.push_back(c);
    int ans=0;
    for(int i=0;i<nms.size()-1;i++){
        ans+=min(nms[i],nms[i+1]);
    }
    return ans;
} 

int main(){
    int n;
    cin>>n;
    vector<int> a(n);
    for(int i=0;i<n;i++)cin>>a[i];
    int p=countUniv(a);
    cout<<p<<"\n";
    return 0;
}
