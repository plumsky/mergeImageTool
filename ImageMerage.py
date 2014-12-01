from PIL import Image
import math

def sortGet(s):
	return s[1]
	
class ImageMerage():
	def __init__(self):
		self.images = []
		self.imagewidth = []
		self.imageheight = []
		self.imageempty = []
		self.reallen = 0
	
	def openImage(self, filelist):
		totalSize = 0
		maxW = 0
		maxH = 0
	
		for f in filelist:
			im = Image.open(f)
			w,h = im.size
			size = w*h
			totalSize += size
			self.images.append((f, size, im))
			self.imagewidth.append((f, w, im))
			self.imageheight.append((f, h, im))
		
			maxW = w if w>maxW else maxW
			maxH = h if h>maxH else maxH
		
		self.mages = sorted(self.images, key=sortGet, reverse=True)
		self.imagewidth = sorted(self.imagewidth, key=sortGet, reverse=True)
		self.imageheight = sorted(self.imageheight, key=sortGet, reverse=True)
	
		half = math.sqrt(totalSize)
		bestSize = 1
		for i in range(1, 20):
			l = 2**i
			if l < half or l < maxW or l < maxH:
				i += 1
			else:
				bestSize = i
				break
		
		self.reallen = 2**bestSize
		
	def findsuitable(self, size):
		for rect in self.imageempty:
			if size[0] <= rect[2] - rect[0] and size[1] <= rect[3] - rect[1]:
				#new empty block
				self.imageempty.append((rect[0], rect[1] + size[1], rect[0] + size[0], rect[3]))
				self.imageempty.append((rect[0] + size[0], rect[1], rect[2], rect[3]))
				destRect = (rect[0], rect[1])
				#remove the old one
				self.imageempty.remove(rect)
                
                #ok we find the suit rect
				return destRect
				
		return None
		
	def meragePic(self, wOrh, out):
		self.destim = Image.new("RGBA", (self.reallen, self.reallen))
		self.imageempty.append((0, 0, self.reallen, self.reallen))
		f = open(out + '.conf', 'w+')
		if wOrh == "height":
			for rect in self.imageheight:
				cSize = rect[2].size
				pos = self.findsuitable(cSize)
				if pos == None:
					print("Make one map failed!")
					return
					
				self.destim.paste(rect[2].convert("RGBA"), pos)
				f.write('{0}	<{1}, {2}, {3}, {4}>\n'.format(rect[0], pos[0], pos[1], cSize[0], cSize[1]))
		else:
			for rect in self.imagewidth:
				cSize = rect[2].size
				pos = self.findsuitable(cSize)
				if pos == None:
					print("Make one map failed!")
					return
					
				self.destim.paste(rect[2].convert("RGBA"), pos)
				f.write('{0}	<{1}, {2}, {3}, {4}>\n'.format(rect[0], pos[0], pos[1], cSize[0], cSize[1]))
				
		self.destim.save(out, "png")
		f.close()
		print("Done!")
	
if __name__ == '__main__':
	img = ImageMerage()
    #Just for test
	img.openImage(("1.png", "2.png"))
	img.meragePic('width', "out.png")
		
