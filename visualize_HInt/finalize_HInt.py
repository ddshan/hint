import os, glob, sys

remove_ls = [
"./TEST_ego4d_img_after/0037b816-e98e-4f54-8046-eb8593b3d127_d60098ce-3716-4e9b-adde-ac8868b57d98_505_pnr_frame_r.crop.jpg",
"./TEST_ego4d_img_after/09e662dd-2324-47d9-99b9-ddd1043b517d_a31fee4e-acce-4513-9ab5-27d3b5484d2c_8852_pre_30_r.crop.jpg",
"./TEST_ego4d_img_after/0bc8996b-85d5-4800-b840-f7ef647a21ee_a48caf98-f1a2-4d0a-83e7-50307d53aefe_4232_post_frame_l.crop.jpg",
"./TEST_ego4d_img_after/29ab413c-dcd0-4b4a-92d6-a49c4095bf28_787762cb-b629-45fb-8f84-9448bc7d0e81_2621_pre_45_l.crop.jpg",
"./TEST_ego4d_img_after/342f509b-4aa9-47f0-8fb2-1efd1f3bdbfa_02af809f-81f2-4f1c-89e2-05c87dd75297_2843_pre_frame_l.crop.jpg",
"./TEST_ego4d_img_after/4726f817-8d28-4e8e-9974-affb07cf4e2b_507630c8-869d-46a4-80f2-ebc0ab5851b5_694_pre_frame_r.crop.jpg",
"./TEST_ego4d_img_after/5012709a-b7e2-430a-92f6-3a87810fb383_15ce85cb-e23e-43d8-b769-08cad307c0a2_2382_post_frame_l.draw.jpg",
"./TEST_ego4d_img_after/779d8772-d716-4db2-883e-831d822e721f_9003ff91-c857-42ea-b55c-84c98f0eb344_3983_pre_45_l.crop.jpg",
"./TEST_ego4d_img_after/87ec3929-5330-4456-9dbb-f42898bf1c23_3e7563f2-44c3-473e-a91e-8eb8e3cec0ae_3172_pre_45_l.crop.jpg",
"./TEST_ego4d_img_after/8d484057-49e2-491c-ae97-c051fa4d06f7_660365d3-6080-4ab2-b2d9-a67f9bc9e83d_3393_pre_45_l.crop.jpg",
"./TEST_ego4d_img_after/935a6367-5ebe-482a-8114-74bd46397a63_ec77c37d-da15-49fa-b00b-f3d373d9fc1e_1908_post_frame_l.crop.jpg",
"./TEST_ego4d_img_after/d334edb4-df15-4373-9865-82053cf185c7_be8868bd-72f8-4abb-94a2-0856be6c5907_4606_post_frame_r.crop.jpg",
"./TEST_ego4d_img_after/d334edb4-df15-4373-9865-82053cf185c7_cb79bc86-882c-4fc6-b779-a607b9008e2e_2106_pre_45_l.crop.jpg",
"./TEST_ego4d_img_after/daff33b7-cf0b-49a9-a5ea-5718f008ed0d_35a418c6-17b5-4ff5-a4ff-14142f03c8a7_1035_pnr_frame_l.crop.jpg",
"./TEST_ego4d_img_after/daff33b7-cf0b-49a9-a5ea-5718f008ed0d_fe922d18-37b8-46e1-a4f4-cec212b2b5a5_4312_pre_45_l.crop.jpg",
"./TEST_ego4d_img_after/e127fc34-0de5-41b0-ab68-7d5574bcf613_669f6183-681c-4287-844f-bd911c9b70c8_2851_pre_15_r.crop.jpg",
"./TEST_ego4d_img_after/f4e2d43a-9fd2-48c0-b1d3-ca32c82ec2c4_a7cf4204-5f76-4819-a906-78133b5e95ff_5634_pre_frame_r.crop.jpg",
"./TEST_hands23_EK_after/EK_0064_P03_10_frame_0000000249_r.crop.jpg",
"./TEST_hands23_ND_after/ND_1_5pHBcVhuU_frame008373_l.crop.jpg",
"./TEST_hands23_ND_after/ND_J6tTGJTQNHU_frame003001_r.draw.jpg",
"./TEST_hands23_ND_after/ND_MMqxuET9zpI_frame009301_l.crop.jpg",
"./TEST_hands23_ND_after/ND__xGfgKCYT7A_frame005751_l.crop.jpg",
"./TEST_hands23_ND_after/ND_hF55RUAGEfA_frame000001_l.crop.jpg",
"./TEST_hands23_ND_after/ND_hF55RUAGEfA_frame000601_l.draw.jpg",
"./TEST_ego4d_seq_after/1b7f6104-363b-4f1e-8552-e9119a0ae8aa_f97735b0-8145-4e27-be40-a47306b047ee_4437_pre_frame_l.crop.jpg",
"./TEST_ego4d_seq_after/989f38a0-db8e-42ce-9361-46825e2f77cb_a3acd6b6-ae64-45f5-98de-731de99eb953_6202_pre_30_r.crop.jpg",
"./TEST_ego4d_seq_after/989f38a0-db8e-42ce-9361-46825e2f77cb_a3acd6b6-ae64-45f5-98de-731de99eb953_6217_pre_15_r.crop.jpg",
"./TEST_ego4d_seq_after/f84f7484-5109-43bc-a54c-7e66478dfb6f_b86aefec-a732-4443-b28d-b148efa77441_788_pre_15_r.crop.jpg"

]
if __name__ == '__main__':
    root  = '/y/dandans/workspace/vis/4Dhands/datatang_data/returned_labels'
    hint_v1 = os.path.join(root, 'handkpts_annotation_v1')
    hint_v2 = os.path.join(root, 'HInt_annotation')
    v1_jpg_ls  = glob.glob(f'{hint_v1}/*/*.jpg')
    v1_json_ls = glob.glob(f'{hint_v1}/*/*.json')
    print(len(v1_jpg_ls), len(v1_json_ls))


    v2_jpg_ls  = glob.glob(f'{hint_v2}/*/*.jpg')
    v2_json_ls = glob.glob(f'{hint_v2}/*/*.json')
    print(len(v2_jpg_ls), len(v2_json_ls))

    # print(f'to remove = {len(remove_ls)}')
    # count = 0
    # for im_path in remove_ls:
    #     _, folder, name = im_path.split('/')
    #     folder = folder.rsplit('_', 1)[0]
    #     name   = name.split('.')[0]
        
    #     jpg_path  = os.path.join(hint_v2, folder, name + '.jpg')
    #     json_path = os.path.join(hint_v2, folder, name + '.json')
    #     if os.path.exists(jpg_path) and os.path.exists(json_path):
    #         count += 1
    #         os.remove(jpg_path)
    #         os.remove(json_path)
            
    # print(f'fount {count}')
    # v2_jpg_ls  = glob.glob(f'{hint_v2}/*/*.jpg')
    # v2_json_ls = glob.glob(f'{hint_v2}/*/*.json')
    # print(len(v2_jpg_ls), len(v2_json_ls))


    # glob.glob()

