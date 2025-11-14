import streamlit as st

from agent import Agent

agent = Agent()
completed_checked = True
learned_checked = False

def header_display():
    st.title("Daily Log Generator")
    st.text("This application is built to streamline the creation of daily work summaries—useful for software engineers, interns, remote teams, or anyone who needs to regularly report progress. It reduces manual writing effort while ensuring logs stay consistent, clear, and professionally formatted.")
    
def input_display(tasks_completed, things_learned):
    global completed_checked
    global learned_checked
    
    learned_input = None
    task_input = None
    
    if tasks_completed:
        completed_checked = True
        task_input = st.text_area("Tasks Completed", placeholder="Researched about...")
    
    if things_learned:
        learned_checked = True
        learned_input = st.text_area("Things Learned", placeholder="Learned how to...")
    
    return task_input, learned_input

def output_display(text):
    st.markdown("### Output")
    st.text(text if text else "Result will show here")
    
def settings_display():
    st.markdown("## Settings")

    st.markdown("#### Fields")
    completed, things_learned = st.columns(2)
    completed_val = completed.checkbox("Tasks Completed", True, "completed")
    things_learned_val = things_learned.checkbox("Things Learned", False, "things_learned")
    
    st.markdown("#### Options")
    next_steps_val = st.checkbox("Suggest Next Steps", False, "next_steps")
    use_bullets = st.checkbox("Use bullets", False, "use_bullets")
    n_of_bullets = 0
    
    
    if use_bullets:
        n_of_bullets = st.number_input("\# of bullets", min_value=1, max_value=5)

    config = {
        "completed": completed_val,
        "things_learned": things_learned_val,
        "next_steps": next_steps_val,
        "use_bullets": use_bullets,
        "n_of_bullets": n_of_bullets
    }

    return any([completed_val, things_learned_val]), config

def generate(text_input, config):
    clicked = st.button("Generate", use_container_width=True)
    
    if clicked:
        text = text_input.title()
        
        result = agent.generate_response(text, config)
        
        result = result.replace("**", "")
        
        return result

def main():
    global completed_checked
    global learned_checked
    
    header_display()
    
    # Controls
    st.divider()
    settings_is_valid, config = settings_display()

    if not settings_is_valid:
        st.error("Select at least 1 field")
        return
    
    # Inputs
    st.divider()
    show_completed = config.get("completed", False)
    show_learned = config.get("things_learned", False)
    task_input, learned_input = input_display(show_completed, show_learned)
    
    if completed_checked and task_input == "" or learned_checked and learned_input == "":
        return
    
    combined_text = ""
    if completed_checked:
        combined_text += f"Tasks Completed:\n{task_input}\n"
    
    if learned_checked:
        combined_text += f"Things Learned:\n{learned_input}\n"

    st.divider()
    result = generate(combined_text, config)
    output_display(result)

main()