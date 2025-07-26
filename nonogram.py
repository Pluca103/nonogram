from itertools import product

# 가능한 줄 배치 생성
def generate_line_possibilities(length, blocks):
    if not blocks:
        return ['.' * length]
    
    total_blocks = sum(blocks)
    min_required_space = total_blocks + (len(blocks) - 1)
    if min_required_space > length:
        return []

    positions = []

    def backtrack(idx, curr, rem_blocks):
        if not rem_blocks:
            curr += '.' * (length - len(curr))
            positions.append(curr)
            return
        for i in range(idx, length - sum(rem_blocks) - len(rem_blocks) + 2):
            new_curr = curr + '.' * (i - len(curr)) + 'X' * rem_blocks[0]
            if len(rem_blocks) > 1:
                new_curr += '.'
            backtrack(i + rem_blocks[0] + 1, new_curr, rem_blocks[1:])

    backtrack(0, '', blocks)
    return positions

# 가능한 배치들 중 공통된 칸만 남기기
def intersect_possibilities(possibilities):
    if not possibilities:return []
    result = []
    for cells in zip(*possibilities):
        if all(c == 'X' for c in cells):
            result.append('X')
        elif all(c == '.' for c in cells):
            result.append('.')
        else:
            result.append('?')
    return result

# 그리드 업데이트
def update_grid(grid, sequences, is_row=True):
    updated = False
    size = len(grid) if is_row else len(grid[0])
    other_size = len(grid[0]) if is_row else len(grid)
    for i in range(size):
        line = grid[i] if is_row else ''.join(grid[j][i] for j in range(other_size))
        known = list(line)
        all_possibilities = generate_line_possibilities(other_size, sequences[i])
        filtered = []
        for p in all_possibilities:
            if all(k == '?' or k == p[j] for j, k in enumerate(known)):
                filtered.append(p)
        inferred = intersect_possibilities(filtered)
        for j in range(other_size):
            if is_row:
                if grid[i][j] != inferred[j]:
                    if grid[i][j] == '?':
                        grid[i][j] = inferred[j]
                        updated = True
            else:
                if grid[j][i] != inferred[j]:
                    if grid[j][i] == '?':
                        grid[j][i] = inferred[j]
                        updated = True
    return updated

# 전체 퍼즐 풀이
def nonoSolve(n, m, row_seq, col_seq):
    grid = [['?' for _ in range(m)] for _ in range(n)]
    changed = True
    while changed:
        changed = update_grid(grid, row_seq, is_row=True)
        changed = update_grid(grid, col_seq, is_row=False) or changed
    return [''.join(row) for row in grid]
###############################################  
def decodeQR(s):
    s=s.split('9')
    N=len(s)//2
    nonoWidth=[]
    for i in range(N):
        a=''
        for j in s[i]:a+=str(int(j)+1)
        nonoWidth.append(a.replace('91','9'))
    nonoHeight=[]
    for i in range(N):
        a=''
        for j in s[i+N]:a+=str(int(j)+1)
        nonoHeight.append(a.replace('91','9'))
    row=[[*map(int,s)]for s in nonoWidth]
    col=[[*map(int,s)]for s in nonoHeight]
    return N,row,col

def printNonogram(row,col,ans,fm=False):
    maxR,maxC=max([*map(len,row)]),max([*map(len,col)])
    if fm:
        for i in ans:print(''.join(i))
    else:
        for i in range(maxC):
            a=''
            for j in col:a+=str(j[i-maxC])if len(j)>=maxC-i else' '
            print(' '*maxR+a)
        for i in range(len(row)):
            print(' '*(maxR-len(row[i]))+''.join(map(str,row[i]))+ans[i])
    print()

s=input()
# 60200069005100902000500020902011110209020110102090020004009600000000069000409002000034090001320109004200000900001002901000102100903010310090221113009401500291310500109113100229021012500091000101130900200123900010002913100102191210051119001142509014300962100019000200000902003000509020112059020001014900230109600070009600130169000201009020520020902010000200920016202090011130096000000000693003290500101009021001911142300910002001109310100113912022109110200409000212319200101111093231021921141102910000320931411093221329311212109000201100019233041932120009601221049000102029020000079020202110209020000200900002209610010
import time
start_tm=time.time()
N,rowQR,colQR=decodeQR(s)

ans=nonoSolve(N,N,rowQR,colQR)
end_tm=time.time()
printNonogram(rowQR,colQR,ans,fm=0)

print(end_tm-start_tm,'s')
