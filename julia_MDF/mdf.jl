using Plots
using JSON


function readJSON(_file::String)
    println(".read")
    open(_file,"r") do f
        data = JSON.parse(f)
        if haskey(data,"points_list")
            ne = size(data["points_list"])[1]
            x0 = Array{Float64}(undef,ne,1)
            y0 = Array{Float64}(undef,ne,1)
            for i=1:ne
                x0[i] = convert(Float64,data["points_list"][i][1])
                y0[i] = convert(Float64,data["points_list"][i][2])
            end
        end
        return ne,x0,y0
    end
end

function outputRes(_res)
    dict = Dict()
    push!(dict,"resultado"=>_res)
    open("output.json","w") do f
        JSON.print(f,dict)
    end
end

function main(_file::String)
    #entrada de dados MDF
    ne, x0, y0 = readJSON(_file)
    conect = [
           0     0    5     2
           1     0    6     3
           2     0    7     4
           3     0    8     0
           0     1    9     6
           5     2   10     7
           6     3   11     8
           7     4   12     0
           0     5   13    10
           9     6   14    11
          10     7   15    12
          11     8   16     0
           0     9    0    14
          13    10    0    15
          14    11    0    16
          15    12    0     0]

    nn = length(conect)
    cc = [
        1  100
        1   75
        1   75
        1    0
        1  100
        0    0
        0    0
        1    0
        1  100
        0    0
        0    0
        1    0
        1  100
        1   25
        1   25
        1    0]

    #resolução MDF
    A = zeros(nn, nn)
    b = zeros(nn, 1)
    bloco = [1, 1, 1, 1]
    for e = 0:nn
        if (cc[e,0]==0)
            A[e,e] = -4
            for j = 0:4
                A[e, conect[e,j]-1] = bloco[j]
            end
        else
            A[e,e] = 1
            b[e,0] = cc[e,1]
        end
    x = b\A
    AA = [-4   1   1   0
           1  -4   0   1
           1   0  -4   1
           0   1   1  -4]

    bb = [-125
           -25
          -175
           -75]

    xx = bb\AA
end


if length(ARGS) == 1
    main(ARGS[1])
end