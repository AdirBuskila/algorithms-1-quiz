#include <stdio.h>
int f(int A[],int size,int k){int low=0,high=size-1;while(low<=high){int mid=low+(high-low)/2;int missing=A[mid]-(mid+1);if(missing<k)low=mid+1;else high=mid-1;}return low+k;}
int g(int A[],int size,int k){int low=0,high=size-1;while(low<=high){int mid=low+(high-low)/2;int missing=A[mid]-(mid+1);if(missing<=k)low=mid+1;else high=mid-1;}return low+k;}
int main(){int A[]={3,5,9,10,11,12};int B[]={2,3,4,7,11};
printf("k=3 -> %d ; k=2 -> %d ; ex(5) -> %d ; buggy ex k=3 -> %d\n",f(A,6,3),f(A,6,2),f(B,5,5),g(B,5,3));
/* exhaustive vs naive */
int bad=0;for(int k=1;k<30;k++){int x=0,c=0;while(1){x++;int in=0;for(int i=0;i<5;i++)if(B[i]==x)in=1;if(!in&&++c==k)break;}if(x!=f(B,5,k))bad++;}
printf("mismatches %d\n",bad);return 0;}
