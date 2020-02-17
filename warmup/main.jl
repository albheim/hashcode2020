
function calc!(path)
    n, p = open("$(path).in") do f
        n, _ = parse.(Int, split(readline(f)))
        p = parse.(Int, split(readline(f)))
        (n, p)
    end

    a = -ones(Int, n)
    b = zeros(Int, n)
    ptr = 0
    for i in p
        print("\r$i/$(p[end]) + $ptr")
        for j in 1:ptr
            if b[j] + i <= n && a[b[j] + i] == -1
                a[b[j] + i] = b[j]
                ptr += 1
                b[ptr] = b[j] + i
            end
        end
        if a[i] == -1
            a[i] = 0
            ptr += 1
            b[ptr] = i
        end
    end

    i = findlast(a .>= 0)
    values = Int[]
    while i != 0
        j = a[i]
        v = i - j
        push!(values, v)
        i = j
    end

    idxs = zero(values)
    ptr = 1
    for i in eachindex(values)
        idxs[i] = findnext(x->x==values[length(values)+1-i], p, ptr)
        ptr = idxs[i] + 1
    end

    open("$(path).out", "w") do io
        write(io, "$(length(idxs))\n$(join(idxs .- 1, " "))\n")
    end
    return sum(values), sum(p[idxs])
end

paths = ["a_example", "b_small", "c_medium", "d_quite_big", "e_also_big"]
calc!(paths[5])
