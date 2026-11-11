#include "core.hpp"
#include <cassert>
#include <cmath>
#include <stdexcept>
#include <limits>
int main(){using namespace lord_sumi;Aggregator a;assert(a.add(10,3));assert(!a.add(10,99));assert(a.add(20,5));auto s=a.summarize(0,30);assert(s.count==2&&s.minimum==3&&s.maximum==5&&s.mean==4);assert(a.summarize(30,40).count==0);bool bad=false;try{a.add(30,std::numeric_limits<double>::infinity());}catch(const std::invalid_argument&){bad=true;}assert(bad);bad=false;try{a.summarize(20,20);}catch(const std::invalid_argument&){bad=true;}assert(bad);}