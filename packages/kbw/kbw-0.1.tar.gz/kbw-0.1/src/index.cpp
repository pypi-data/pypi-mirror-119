/* Copyright 2020, 2021 Evandro Chagas Ribeiro da Rosa <evandro.crr@posgrad.ufsc.br>
 * Copyright 2020, 2021 Rafael de Santiago <r.santiago@ufsc.br>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "../include/ket_bitwise.hpp"
#include <iostream>
#include <bitset>

using namespace ket;

void Index::flip(size_t idx) {
    data[idx/64] ^= 1ull << (idx%64); 
}

bool Index::is_one(size_t idx) const {
    return data[idx/64] & (1ull << (idx%64));
}

bool Index::is_zero(size_t idx) const {
    return not (data[idx/64] & (1ull << (idx%64)));
}


uint64_t Index::operator[](size_t idx) const {
    return data[idx];
}

uint64_t& Index::operator[](size_t idx) {
    return data[idx];
}

Index Index::operator|(const Index& other) const {
    Index result;
    for (size_t i = 0; i < Index::size; i++) 
        result.data[i] = data[i] | other.data[i];
    return result;
}

bool Index::operator<(const Index& other) const {
    for (size_t i = 0; i < size; i++) {
        if (data[i] < other.data[i]) return true;
        else if (data[i] > other.data[i]) return false;
    }
    return false;
}

size_t ket::hash_value(const Index& idx) {
    size_t aux = 0;
    boost::hash<uint64_t> ui64_hash;
    for (size_t i = 0; i < idx.size; i++) {
        aux ^= ui64_hash(idx[i]);
    }
    return aux;
}

bool ket::operator==(const Index& a, const Index& b) {
    for (size_t i = 0; i < a.size; i++) {
        if (a[i] != b[i]) {
            return false;
        }
    }
    return true;
}

std::ostream& ket::operator<<(std::ostream &os, const Index& idx) {
    for (size_t i = idx.size; i > 0; --i) {
        std::bitset<64> bits(idx[i-1]);
        os << bits;
    }
    return os;
}
