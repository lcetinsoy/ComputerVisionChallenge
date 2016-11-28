require 'torch'
require 'image'
require 'nn'
net = torch.load('../input/VGG_FACE.t7')
net:evaluate()


input = csvfile.read('../output/cleaned.csv')

function table.shallow_copy(t)

  local t2 = {}
  for i=1, 4096 do
    t2[#t2 + 1] = t[i]
  end
  return t2
end


output = nil
output = {}
path="/home/nawel/Downloads/wiki/wiki_crop/"
print(output, #output)
for i=2,#input do
    im = nil
    im_scaled = nil
    im_bgr = nil
    features = nil

    im = image.load(path .. input[i][5],3,'float')

    im_scaled = image.scale(im,"224x224")
    im_scaled = im_scaled*255

    mean = {129.1863,104.7624,93.5940}
    im_bgr = im_scaled:index(1,torch.LongTensor{3,2,1})
    for h = 1, 3 do
        im_bgr[h]:add(-mean[h])
    end
    features=net(im_bgr)

    --table.insert(output, features )--output[i-1]=net(im_bgr)
    output[#output + 1] = table.shallow_copy(features)
    --print(#output, output, features[1], features[545])
end