%module opgraph

%include "std_vector.i"

%{
#include "opgraph.h"
%}

namespace std{
        %template(IntV) vector<int>;
        %template(OpV) vector<Operator>;
}

%include "opgraph.h"
