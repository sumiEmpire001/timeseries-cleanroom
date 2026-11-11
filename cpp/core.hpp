#pragma once
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <map>
#include <stdexcept>
namespace lord_sumi {
struct Summary {std::size_t count=0;double minimum=0,maximum=0,mean=0;};
class Aggregator {
 std::map<std::int64_t,double> samples_;
 public:
 bool add(std::int64_t epoch_seconds,double value){
  if(!std::isfinite(value))throw std::invalid_argument("nonfinite sample");
  return samples_.emplace(epoch_seconds,value).second;
 }
 std::size_t size()const{return samples_.size();}
 Summary summarize(std::int64_t start_inclusive,std::int64_t end_exclusive)const{
  if(start_inclusive>=end_exclusive)throw std::invalid_argument("invalid interval");
  Summary s;double total=0;
  for(auto it=samples_.lower_bound(start_inclusive);it!=samples_.end()&&it->first<end_exclusive;++it){
   const double x=it->second;if(!s.count)s.minimum=s.maximum=x;
   else{if(x<s.minimum)s.minimum=x;if(x>s.maximum)s.maximum=x;}
   ++s.count;total+=x;if(!std::isfinite(total))throw std::overflow_error("sum overflow");
  }
  if(s.count)s.mean=total/static_cast<double>(s.count);
  return s;
 }
};
}