import numpy as np
from . import morph as morph

def stage_1(img):
	patterns = []

	# bond = 1
	s1 = []
	patterns.append(s1)

	# bond = 2
	s2 = []
	patterns.append(s2)

	# bond = 3
	s3 = []
	patterns.append(s3)

	# bond = 4
	s4 = [0b010011000, 0b010110000, 0b000110010, 0b000011010, 0b001011001, 0b111010000, 0b100110100, 0b000010111]
	patterns.append(s4)

	# bond = 5
	s5 = []
	patterns.append(s5)

	# bond = 6
	s6 = [0b111011000, 0b011011001, 0b111110000, 0b110110100, 0b100110110, 0b000110111, 0b000011111, 0b001011011]
	patterns.append(s6)

	# bond = 7
	s7 = [0b111011001, 0b111110100, 0b100110111, 0b001011111]
	patterns.append(s7)

	# bond = 8
	s8 = [0b011011011, 0b111111000, 0b110110110, 0b000111111]
	patterns.append(s8)

	# bond = 9
	s9 = [0b111011011, 0b011011111, 0b111111100, 0b111111001, 0b111110110, 0b110110111, 0b100111111, 0b001111111]
	patterns.append(s9)

	# bond = 10
	s10 = [0b111011111, 0b111111101, 0b111110111, 0b101111111]
	patterns.append(s10)

	# bond = 11
	s11 = [0b111111011, 0b111111110, 0b110111111, 0b011111111]
	patterns.append(s11)

	conditional_mark = np.zeros_like(img)
	img_bond = morph.cal_bond(img)
	
	h, w = img.shape
	ext_img = np.zeros([h+2, w+2])
	ext_img[1:h+1, 1:w+1] = img

	pixel_stack = np.zeros([h, w]).astype(int)

	for i in range(h):
		for j in range(w):
			for m in range(3):
				for n in range(3):
					pixel_stack[i, j] = pixel_stack[i, j] << 1
					if ext_img[i+m, j+n] > 0:
						pixel_stack[i, j] = pixel_stack[i, j] + 1
	# find removable candidates
	for i in range(h):
		for j in range(w):
			if img_bond[i, j] >= 4 and img_bond[i, j] <= 11:
				for s in (patterns[img_bond[i, j]-1]):
					if s == pixel_stack[i, j]:
						conditional_mark[i, j] = 1
						break
	return conditional_mark

def check_patterns_1(p_hit, conditional_mark, pixel_stack, patterns_1):
	h, w = p_hit.shape
	for i in range(h):
		for j in range(w):
			if p_hit[i, j] == 1 or conditional_mark[i, j] == 0:
				continue
			for p1 in patterns_1:
				for p in p1:
					if pixel_stack[i, j] == p:
						p_hit[i, j] = 1
						break
				if (p_hit[i, j] == 1):
					break

def check_patterns_2(p_hit, conditional_mark, pixel_stack, patterns_2):
	h, w = p_hit.shape
	for i in range(h):
		for j in range(w):
			if p_hit[i, j] == 1 or conditional_mark[i, j] == 0:
				continue
			for p2 in patterns_2:
				length = len(p2[0])
				for k in range(length):
					if (((pixel_stack[i, j] & p2[0][k]) ^ p2[1][k]) != 0):
						continue
					elif (pixel_stack[i, j] & p2[2][k] > 0):
						p_hit[i, j] = 1
						break
				if (p_hit[i, j] == 1):
					break

def check_patterns_3(p_hit, conditional_mark, pixel_stack, patterns_3):
	h, w = p_hit.shape
	for i in range(h):
		for j in range(w):
			if p_hit[i, j] == 1 or conditional_mark[i, j] == 0:
				continue
			for p3 in patterns_3:
				for p in p3:
					if (((pixel_stack[i, j] & p) ^ p) == 0):
						p_hit[i, j] = 1
						break
				if (p_hit[i, j] == 1):
					break

def check_patterns_4(p_hit, conditional_mark, pixel_stack, patterns_4):
	h, w = p_hit.shape
	for i in range(h):
		for j in range(w):
			if p_hit[i, j] == 1 or conditional_mark[i, j] == 0:
				continue
			for p4 in patterns_4:
				length = len(p4[0])
				for k in range(length):
					if (((pixel_stack[i, j] & p4[0][k]) ^ p4[1][k]) == 0):
						p_hit[i, j] = 1
						break
				if (p_hit[i, j] == 1):
					break

def stage_2(img, conditional_mark):
	patterns_1 = [] # M
	patterns_2 = [] # M, A, B, C, 0
	patterns_3 = [] # M, D
	patterns_4 = [] # M, D, 0

	spur = []
	spur.append(0b000010001)
	spur.append(0b000010100)
	spur.append(0b001010000)
	spur.append(0b100010000)
	patterns_1.append(spur)

	four_connected_offset = []
	four_connected_offset.append(0b000010010)
	four_connected_offset.append(0b000011000)
	four_connected_offset.append(0b000110000)
	four_connected_offset.append(0b010010000)
	patterns_1.append(four_connected_offset)

	L_corner = []
	L_corner.append(0b010011000)
	L_corner.append(0b010110000)
	L_corner.append(0b000011010)
	L_corner.append(0b000110010)
	patterns_1.append(L_corner)

	vee_branch = []
	pre_and = [0b101010000, 0b100010100, 0b000010101, 0b001010001]
	M_xor = [0b101010000, 0b100010100, 0b000010101, 0b001010001]
	AB_and = [0b000000111, 0b001001001, 0b111000000, 0b100100100]
	vee_branch.append(pre_and)
	vee_branch.append(M_xor)
	vee_branch.append(AB_and)
	patterns_2.append(vee_branch)

	corner_cluster = []
	corner_cluster.append(0b011011000)
	corner_cluster.append(0b000110110)
	corner_cluster.append(0b110110000)
	corner_cluster.append(0b000011011)
	patterns_3.append(corner_cluster)

	tee_branch = []
	pre_and = [0b010111011, 0b010110010, 0b000111010, 0b010011010]
	M_xor = [0b010111000, 0b010110010, 0b000111010, 0b010011010]
	tee_branch.append(pre_and)
	tee_branch.append(M_xor)
	patterns_4.append(tee_branch)

	diagonal_branch = []
	pre_and = [0b011111110, 0b110111011, 0b011111110, 0b110111011]
	M_xor = [0b010011100, 0b010110001, 0b001110010, 0b100011010]
	diagonal_branch.append(pre_and)
	diagonal_branch.append(M_xor)
	patterns_4.append(diagonal_branch)

	# pixel stack
	pixel_stack = np.zeros(img.shape).astype(int)
	h, w = img.shape
	ext_c_img = np.zeros([h+2, w+2])
	ext_c_img[1:h+1, 1:w+1] = conditional_mark

	for i in range(h):
		for j in range(w):
			for m in range(3):
				for n in range(3):
					pixel_stack[i, j] = pixel_stack[i, j] << 1
					if ext_c_img[i+m, j+n] == 1:
						pixel_stack[i, j] = pixel_stack[i, j] + 1
	# hit or not
	p_hit = np.zeros_like(img)
	check_patterns_1(p_hit, conditional_mark, pixel_stack, patterns_1)
	check_patterns_2(p_hit, conditional_mark, pixel_stack, patterns_2)
	check_patterns_3(p_hit, conditional_mark, pixel_stack, patterns_3)
	check_patterns_4(p_hit, conditional_mark, pixel_stack, patterns_4)

	# sk_img (skeletonized image)
	sk_img = np.zeros_like(img)
	binary_img = np.zeros_like(img)
	binary_img[img >= 100] = 1
	binary_img[img < 0] = 0
	for i in range(h):
		for j in range(w):
			sk_img[i, j] = binary_img[i, j] & ((conditional_mark[i, j] ^ 1) | p_hit[i, j])
	for i in range(h):
		for j in range(w):
			if sk_img[i, j] == 1:
				sk_img[i, j] = 255
			else:
				sk_img[i, j] = 0
	return sk_img


def cal_255(img):
	count = 0
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if (img[i, j] > 0):
				count += 1
	return count

def skeletonize(img):
	pre_sk = img.astype(np.uint8)
	rounds = 0
	H = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
	while True:
		if (rounds <= 20 and rounds % 10 == 0) or rounds % 20 == 0:
			# find removable candidates
			d_img = morph.dilation(pre_sk, H).astype(np.uint8)
			conditional_mark = stage_1(d_img)
			# confirm the remove operation
			sk_img = stage_2(d_img, conditional_mark)
			sk_img = sk_img.astype(np.uint8)
			if (sk_img == d_img).all():
				break
			else:
				pre_sk = sk_img
		else:
			# find removable candidates
			conditional_mark = stage_1(pre_sk)
			# confirm the remove operation
			sk_img =  stage_2(pre_sk, conditional_mark)
			sk_img = sk_img.astype(np.uint8)
			if (sk_img == pre_sk).all():
				break
			else:
				pre_sk = sk_img
		
		print(cal_255(sk_img))
		rounds += 1
	return sk_img
