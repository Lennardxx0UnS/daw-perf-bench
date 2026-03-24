import math
import time
import sys # 新增 sys 模块用于处理命令行参数

def calculate_daw_performance(cb_st, cb_mt, gb_comp, gb_photo, gb_blur, gb_text, l3_size_mb, mem_bw_gbps):
    """底层三大音频场景算力内核"""
    # 锚点基准: Apple M1 (8 Core, 8GB) = 1.00x 基准线
    A_cb_st, A_cb_mt = 427, 1689
    A_gb_comp, A_gb_photo = 10547, 2910
    A_gb_blur, A_gb_text = 2152, 2340
    
    r_cb_st = cb_st / A_cb_st
    r_cb_mt = cb_mt / A_cb_mt
    r_gb_comp = gb_comp / A_gb_comp
    r_gb_photo = gb_photo / A_gb_photo
    r_gb_blur = gb_blur / A_gb_blur
    r_gb_text = gb_text / A_gb_text
    
    k_mem = 1 + 0.25 * math.log10(mem_bw_gbps / 50)
    k_cache = 1 + 0.05 * math.log2(l3_size_mb / 16)
    
    score_orch = ((0.4 * r_cb_mt) + (0.4 * r_gb_comp)) * k_mem * k_cache + (0.2 * r_gb_text)
    score_mix = (0.2 * r_cb_st) + (0.3 * r_gb_photo) + (0.5 * r_gb_blur)
    score_live = (0.6 * r_gb_text) + (0.2 * r_gb_photo) + (0.2 * r_cb_st)
    
    return score_orch, score_mix, score_live

def evaluate_user_experience(score_orch, score_mix, score_live, wa, wb, wc):
    """执行柯布-道格拉斯非线性加权与动态 UX Sigmoid 流程度映射"""
    if abs((wa + wb + wc) - 1.0) > 0.01:
        raise ValueError("三大场景权重之和必须等于 1.0")
    
    # 计算综合几何指数
    s_user = (score_orch ** wa) * (score_mix ** wb) * (score_live ** wc)
    
    # 动态 S 型曲线拐点校准 (已修复为真实及格线)
    beta_orch_base = 1.4   # 多轨及格线
    beta_mix_base = 1.15   # 混音及格线
    beta_live_base = 0.95  # 实录及格线
    
    beta_dynamic = (beta_orch_base ** wa) * (beta_mix_base ** wb) * (beta_live_base ** wc)
    
    # 动态映射
    ux_score = 100 / (1 + math.exp(-3.5 * (s_user - beta_dynamic)))
    return s_user, ux_score

def get_float_input(prompt_text):
    """安全获取用户输入的辅助函数"""
    while True:
        try:
            return float(input(prompt_text))
        except ValueError:
            print("⚠️ 输入无效，请输入一个纯数字！")

def run_interactive_mode():
    """无参数时的交互式向导模式 (您原本的逻辑)"""
    print("=" * 60)
    print(" 🎹 DAW 硬件底层算力与 UX 体验交互式评估系统 (v1.0)")
    print("=" * 60)
    
    print("\n>>> [1/3] 请输入目标 CPU 的基准参数 <<<")
    cb_st = get_float_input("1. Cinebench 单核分数 (例: 536) : ")
    cb_mt = get_float_input("2. Cinebench 多核分数 (例: 5262): ")
    gb_comp = get_float_input("3. Geekbench 6 资产压缩 (例: 28813): ")
    gb_photo = get_float_input("4. Geekbench 6 照片滤镜 (例: 4037) : ")
    gb_blur = get_float_input("5. Geekbench 6 背景模糊 (代理AVX/AMX, 例: 4695): ")
    gb_text = get_float_input("6. Geekbench 6 文本处理 (例: 3597) : ")
    l3_size_mb = get_float_input("7. L3 缓存大小 / Apple SLC 容量 (MB, 例: 32): ")
    mem_bw_gbps = get_float_input("8. 内存物理总带宽 (GB/s, 例: 100) : ")

    print("\n" + "=" * 60)
    print(">>> [2/3] 请配置您的专属工程权重 <<<")
    print("💡 【常见曲风与干活习惯权重参考】")
    print(" 🎻 好莱坞配乐 (重吞吐): Wa=0.70, Wb=0.20, Wc=0.10")
    print(" 🎸 日系摇滚/J-Pop (重混音): Wa=0.20, Wb=0.55, Wc=0.25")
    print(" 🎧 卧室全栈制作人 (综合型): Wa=0.20, Wb=0.50, Wc=0.30")
    print("-" * 60)

    while True:
        wa = get_float_input("👉 输入多轨管弦权重 Wa (0~1): ")
        wb = get_float_input("👉 输入单轨混音权重 Wb (0~1): ")
        wc = get_float_input("👉 输入低延迟实录权重 Wc (0~1): ")
        if abs((wa + wb + wc) - 1.0) < 0.01:
            break
        print(f"❌ 【校验失败】总和为 {wa+wb+wc:.2f}，不等于 1.0！请重新分配。")

    print("\n🚀 正在重构硬件算力模型...")
    time.sleep(1) 
    print_results(cb_st, cb_mt, gb_comp, gb_photo, gb_blur, gb_text, l3_size_mb, mem_bw_gbps, wa, wb, wc)

def run_cli_mode(args):
    """带参数时的一次性快速计算模式"""
    try:
        # 将传入的字符串参数转化为浮点数
        cb_st, cb_mt, gb_comp, gb_photo = float(args[0]), float(args[1]), float(args[2]), float(args[3])
        gb_blur, gb_text, l3_size_mb, mem_bw_gbps = float(args[4]), float(args[5]), float(args[6]), float(args[7])
        wa, wb, wc = float(args[8]), float(args[9]), float(args[10])
    except ValueError:
        print("❌ 参数格式错误！请确保输入的11个参数均为纯数字。")
        return

    if abs((wa + wb + wc) - 1.0) > 0.01:
        print(f"❌ 【权重校验失败】输入的 Wa({wa}) + Wb({wb}) + Wc({wc}) 总和为 {wa+wb+wc:.2f}，必须等于 1.0！")
        return

    print_results(cb_st, cb_mt, gb_comp, gb_photo, gb_blur, gb_text, l3_size_mb, mem_bw_gbps, wa, wb, wc)

def print_results(cb_st, cb_mt, gb_comp, gb_photo, gb_blur, gb_text, l3_size_mb, mem_bw_gbps, wa, wb, wc):
    """统一的结果输出模块"""
    orch, mix, live = calculate_daw_performance(cb_st, cb_mt, gb_comp, gb_photo, gb_blur, gb_text, l3_size_mb, mem_bw_gbps)
    s_user, ux_score = evaluate_user_experience(orch, mix, live, wa, wb, wc)
    
    print("\n" + "=" * 60)
    print("📊 【第一步：基础场景相对算力 (对比 M1 基准)】")
    print(f" 🎵 多轨并行 (Orchestral) : {orch:.2f}x")
    print(f" 🎛️ 单轨串行 (Mix DSP)    : {mix:.2f}x")
    print(f" 🎸 低延迟响应 (Live)     : {live:.2f}x")
    
    print("\n🎯 【第二步：专属 UX 流程度评估】")
    print(f" 综合几何指数 (Cobb-Douglas) : {s_user:.2f}")
    print(f" 最终 UX 体感得分 (Sigmoid)  : {ux_score:.1f} / 100")
    
    print("\n🏆 >>> DAW 真实生存处境评定 <<<")
    if ux_score >= 95:
        print("【Tier 1: 算力过剩期 (God Mode)】畅通无阻，彻底告别冻结！")
    elif ux_score >= 80:
        print("【Tier 2: 灵感涌现期 (The Flow State)】百轨工程丝滑运行，硬件无感化。")
    elif ux_score >= 50:
        print("【Tier 3: 妥协平衡期 (The Compromise)】日常流畅，重度总线处理需增加缓冲。")
    else:
        print("【Tier 4: 挣扎求生期 (The Struggle)】极易爆音，需频繁依赖原地渲染与冻结。")
    print("=" * 60)

if __name__ == "__main__":
    # sys.argv 列表包含了命令行传入的所有内容
    # sys.argv[0] 永远是脚本名字 (如 WHITEPAPER1.1.PY)
    # 后面的才是我们输入的参数
    
    total_args = len(sys.argv) - 1 

    if total_args == 0:
        # 没有任何参数，进入交互指导模式
        run_interactive_mode()
    elif total_args == 11:
        # 精准传入了 11 个参数，进入极速 CLI 模式
        run_cli_mode(sys.argv[1:])
    else:
        # 乱输参数，弹出说明书
        print("\n❌ 参数数量错误！您输入了 {} 个参数，程序需要严格的 11 个参数。".format(total_args))
        print("=" * 60)
        print("👉 【用法 1: 交互向导模式】(适合新手)")
        print("python WHITEPAPER1.1.PY")
        print("\n👉 【用法 2: 一次性快速计算模式】(适合极客)")
        print("python WHITEPAPER1.1.PY <单核> <多核> <压缩> <滤镜> <模糊> <文本> <L3缓存> <内存带宽> <Wa权重> <Wb权重> <Wc权重>")
        print("\n📝 示例代码:")
        print("python WHITEPAPER1.1.PY 440 4000 17935 2828 3120 2454 16 80 0.4 0.4 0.2")
        print("=" * 60)