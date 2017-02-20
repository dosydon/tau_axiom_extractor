#include <vector>
using namespace std;

class Operator{
	public:
		vector<int> eff_var;
		vector<int> req_var;
		Operator() {}
		Operator(vector<int>& e,vector<int>& r) {
			eff_var = e;
			req_var = r;
		}
		void print(){
			for(int i = 0; i < eff_var.size();i++){
				cout << eff_var[i] << endl;
			}
		}
};

void read();
void construct(vector<Operator>& ops);
vector<int> get_candidates(vector<Operator>& ops);
