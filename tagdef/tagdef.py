import numpy as np
import drawsvg
import cv2
class TagDefine:
    area = 16
    ham = 5
    dim = 4
    codes = (0x231b, 0x2ea5, 0x346a, 0x45b9, 0x79a6, 0x7f6b, 0xb358, 0xe745, 0xfe59, 0x156d, 0x380b, 0xf0ab, 0x0d84, 0x4736, 0x8c72,
             0xaf10, 0x093c, 0x93b4, 0xa503, 0x468f, 0xe137, 0x5795, 0xdf42, 0x1c1d, 0xe9dc, 0x73ad, 0xad5f, 0xd530, 0x07ca, 0xaf2e)
    def get_numpy(self,index):
        code = self.codes[index]
        d = np.frombuffer(np.array(code, ">i8"), np.uint8)
        bits = np.unpackbits(d)[-self.area:].reshape((-1,self.dim))
        tag = np.pad(bits, 1, 'constant', constant_values=0)*255
        return tag
    
    def get_svg(self,index,size) -> drawsvg.Group:
        svg=drawsvg.Group(id=f"tag{index}",style="stroke-width:0;stroke-dasharray:none" )
        tag=self.get_numpy(index)
        unit=float(size)/(self.dim+2)
        for i in range(self.dim+2):
            for j in range(self.dim+2):
                if tag[i,j] == 255:
                    svg.append(drawsvg.Rectangle(j*unit,i*unit,unit,unit,fill='white',style="stroke-width:0;stroke-dasharray:none"))
                else:
                    svg.append(drawsvg.Rectangle(j*unit,i*unit,unit,unit,fill='black',style="stroke-width:0;stroke-dasharray:none"))
        return svg
    
    def test(self):
        tag=self.get_numpy(0)
        svg=self.get_svg(0)
        svg_pic=drawsvg.Drawing(10,10)
        svg_pic.append(svg)
        svg_pic.save_svg("tag.svg")
        cv2.imshow("img",tag)
        cv2.waitKey(0)
