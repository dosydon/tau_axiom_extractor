#include <lemon/list_graph.h>
#include <lemon/connectivity.h>
#include <time.h>
#include <stdio.h>
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include "opgraph.h"
using namespace lemon;
using namespace std;
int N;
vector< vector<int> > EFF_VARS;
vector< vector<int> > REQUIREMENT_VARS;
vector<ListDigraph::Node> V;
ListDigraph G;
ListDigraph::NodeMap<int> CON(G);

void read(){
	cin >> N;
	int num_var;
	int var;
	for(int i = 0; i < N;i++){
		cin >> num_var;
		vector<int> temp;
		REQUIREMENT_VARS.push_back(temp);
		for(int j = 0; j < num_var;j++){
			cin >> var;
			REQUIREMENT_VARS[i].push_back(var);
		}
		cin >> num_var;
		vector<int> temp2;
		EFF_VARS.push_back(temp2);
		for(int j = 0; j < num_var;j++){
			cin >> var;
			EFF_VARS[i].push_back(var);
		}
	}
}
void construct(vector<Operator>& ops){
	for(int i =0; i < ops.size();i++){
		V.push_back(G.addNode());
	}
	for(int i = 0;i < ops.size();i++){
		for(int j = 0; j < ops.size();j++){
			if(i != j){
				if(!includes(ops[j].req_var.begin(),ops[j].req_var.end(),
							ops[i].eff_var.begin(),ops[i].eff_var.end())){
					G.addArc(V[i],V[j]);
				}
			}
		}
	}
}

vector<int> get_candidates(vector<Operator>& ops){
	vector<int> res;
	construct(ops);
	stronglyConnectedComponents(G,CON);
	for(int i=0;i < V.size();i++){
		if(CON[V[i]] > 0)
			res.push_back(i);
	}
	return res;
}




int main(int argc, char* argv[]) {
// 	read();
// 	vector<int> res = get_candidates(EFF_VARS,REQUIREMENT_VARS);
// 	for(int i = 0; i < res.size();i++){
// 		cout << res[i] << endl;
// 	}
	return 0;
}
